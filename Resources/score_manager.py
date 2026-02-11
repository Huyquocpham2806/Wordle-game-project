from structures import SortedLinkedList
from security import xor_string

ScoreFile = "leaderboard.txt"

class ScoreManager:
    """
    Class quản lý dữ liệu người chơi.
    Sử dụng cấu trúc dữ liệu: Sorted Linked List (Danh sách liên kết đã sắp xếp).
    Mục đích: Giữ cho danh sách luôn được sắp xếp theo thời gian chơi (từ thấp đến cao)
    ngay cả khi thêm mới hoặc cập nhật điểm.
    """
    def __init__(self):
        self.users = SortedLinkedList()
        self.load_data()

    # Hàm tải dữ liệu từ file leaderboard.txt và lưu vào cấu trúc dữ liệu
    def load_data(self):
        """
        Đọc dữ liệu từ file text, giải mã và đưa vào Linked List.
        Sử dụng encoding='utf-8' để tránh lỗi font chữ trên Windows.
        """
        try: 
            with open(ScoreFile, 'r', encoding='utf-8') as Scoreinp:
                lines = Scoreinp.readlines()

            for line in lines:
                """
                Ở đây sử dụng thuật toán XOR để giải mã dữ liệu trước khi xử lí
                Thuật toán nằm trong file security.py
                """
                decodeline = xor_string(line.strip())

                parts = decodeline.split("|")

                # Dữ liệu của người chơi phải đủ 5 yếu tố trong format chuẩn: 
                # Tên, mật khẩu, điểm (là thời gian trung bình), tổng thời gian chơi (chỉ những ván thắng), tổng số ván đã thắng
                if len(parts) >= 5: 
                    name = parts[0]
                    password = parts[1]
                    score = float(parts[2])      
                    total_time = float(parts[3]) 
                    total_game = int(parts[4])   

                    # Chèn thông tin người chơi vào danh sách 
                    # Dùng hàm insert_sorted của SortedLinkList() để quản lí
                    self.users.insert_sorted(name, password, score, total_time, total_game)
        except FileNotFoundError: # tự tạo file leaderboard.txt mới khi không kiếm thấy file
            with open('leaderboard.txt', 'w', encoding = 'utf-8') as f:
                pass 
        except Exception as e:
            print(f'error loading data: {e}')
    
    # Hàm lưu dữ liệu từ cấu trúc dữ liệu vào file leaderboard.txt
    def save_to_file(self):
        """
        Hàm này dùng để lưu toàn bộ danh sách liên kết xuống file leaderboard.txt
        Quy trình: Linked List -> List -> Mã hóa XOR -> Ghi file
        """
        # Chuyển đổi Linked List thành List để dễ duyệt
        data_list = self.users.to_list()
        
        with open(ScoreFile, 'w', encoding='utf-8') as f:
            for user in data_list:
                # Format chuẩn: tên|mật khẩu|điểm|thời gian chơi|tổng số ván thắng
                line = f"{user['name']}|{user['pass']}|{user['score']}|{user['total_time']}|{user['total_game']}"
                
                # Tiếp tục dùng thuật toán XOR để mã hóa dữ liệu
                encodeline = xor_string(line)
                f.write(encodeline + "\n") # Thêm '\n' ở cuối để tự động xuống dòng

    # Hàm đăng ký tài khoản mới cho người chơi
    def register(self, name, password):
        """
        Hàm này dùng để đăng ký tài khoản mới.
        Các bước kiểm tra cần có:
        - Nếu tên người chơi đã có trong danh sách (tức là bị trùng), hàm sẽ trả về False
        - Nếu tên người chơi chưa có, thì có thể đăng kí mới
        """
        if self.users.find_user(name): 
            return False, 'Name already exists'
        
        # Dùng hàm inser_sorted() trong SortLinkedList()
        self.users.insert_sorted(name, password, 0, 0, 0)
        self.save_to_file()
        return True, 'Register success'

    # Hàm đăng nhập cho người chơi
    def login(self, name, password):
        """
        Hàm này dùng để xác thực đăng nhập.
        Các bước thực hiện:
        - Hàm này sẽ dùng hàm find_user() trong SortedLinkedList() để tìm têm người chơi
        - Nếu tên người chơi có tồn tại, tiếp tục kiểm tra mật khẩu
        """

        # Dùng hàm find_user() trong SortLinkedList() để tìm tên người chơi
        user = self.users.find_user(name) 
        if user:
            if user['pass'] == password:
                return True, 'Login success'
            else:
                return False, 'Wrong password'
        return False, 'User not found'

    # Hàm cập nhật điểm số của người chơi sau mỗi lần chơi xong
    def update_score(self, name, time):
        """
        Hàm này dùng để cập nhật thành tích người chơi sau khi thắng game

        Cách hoạt động:
        - Danh sách người chơi được quản lí bởi SortedLinkList(), 
        nên khi điểm người chơi thay đổi, điểm sẽ thay đổi thông qua hàm này

        - Nhưng khi thay đổi điểm thì thứ tự trên bản xếp hạng chưa được sắp xếp lại

        - Nên sau khi cập nhật điểm, hàm này sẽ dùng hàm remove() trong SortedLinkedList() để xóa node cũ
        và thêm lại node mới, việc sắp xếp sẽ do hàm insert_sorted() quản lí
        """

        # Dùng hàm get_node() trong SortedLinkedList() để tìm thông tin người chơi thông qua name
        user_node = self.users.get_node(name)
        
        # Bước cập nhật điểm
        if user_node:
            # cập nhật các thông tin có thay đổi
            saved_pass = user_node.password
            new_total_game = user_node.total_games + 1
            new_total_times = user_node.total_time + time
            
            # Tính điểm trung bình mới
            new_avg_score = round(new_total_times/new_total_game, 2)

            # Bước xóa node cũ
            self.users.remove(name)

            # Bước thêm node mới và sắp xếp lại
            self.users.insert_sorted(name, saved_pass, new_avg_score, new_total_times, new_total_game)
            # Lưu xuống file để chắc chắn danh sách đã được cập nhật
            self.save_to_file() 

    # Hàm lấy top 20 người chơi có điểm số tốt nhất (thời gian trung bình thấp nhất)
    def get_top(self):
        """
        Hàm này đùng dể lấy danh sách Top 20 người chơi xuất sắc nhất.
        Vì sẽ có những người chơi rất nhiều nhưng có khi chưa thắng được ván nào,
        nên cần phải có thêm một bước để đảm bảo total_game > 0
        """
        full_list = self.users.to_list()
        
        # bước kiểm tra cuối cùng
        valid_list = [user for user in full_list if user['total_game'] > 0]
        
        # Dùng kĩ thuật Slicing để lấy top 20 người đầu tiên
        return valid_list[:20]
