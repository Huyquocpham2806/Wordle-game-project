import random
import resume
from settings import *
from structures import Stack

class WordleGame:
    """
    Class trung tâm xử lý toàn bộ logic của game.
    Chịu trách nhiệm về:
    - Quản lý trạng thái (State): Đang chơi, thắng, thua.
    - Xử lý dữ liệu (Data): Load từ vựng, kiểm tra từ hợp lệ.
    - Thuật toán: Tô màu (check_guess), Gợi ý (Hint), Hoàn tác (Undo).
    """
    def __init__(self, mode='WORD', difficulty = 'EASY'):
        self.mode = mode                                # Chế độ chơi: "WORD" hoặc "MATH"
        self.difficulty = difficulty                    # Độ khó: "EASY" hoặc "HARD" (chỉ dùng cho WORD)

        # Biến lưu danh sách đáp án, và đáp án hợp lệ
        self.solutions, self.valid_guesses = None, None 
        self.load_data()

        # Các biến trạng thái game
        self.hint_used = 0          # Số lần dùng gợi ý
        self.guesses = []           # List chưa các từ người chơi đã đoán
        self.current_guess = ""     # Từ người chơi đang nhập hiện tại

        # Chọn ngẫu nhiên đáp án
        self.ans = random.choice(self.solutions).upper()      

        # Biến lưu kết quả
        # Gồm 3 trạng thái: 
        # - "": Đang chơi
        # - "w": Thắng
        # - "l": Thua
        self.result = ""

        self.reset_key_color() # Khởi tạo lại màu của bàn phím

        # Dùng Stack để lưu lịch sử (dùng để sử dụng chức năng undo)
        self.history_stack = Stack()
    
    # Hàm tải dữ liệu từ dataset
    def load_data(self):
        """
        Hàm dùng để đọc dữ liệu từ file text dựa trên chế độ chơi là "MATH" hay "WORD
        """
        if self.mode == 'WORD':
            if self.difficulty == "EASY":
                # Chọn file dựa trên độ khó
                file_path = 'English (EZ dataset).txt'
            else:
                file_path = 'English (Hard dataset).txt'
            
            with open(file_path, 'r', encoding= 'utf-8') as inp:
                data = [word.strip().upper() for word in inp.readlines()]

            # Gộp 2 file lại để tạo một cuốn từ điển hợp lệ
            with open('English (Hard dataset).txt', 'r', encoding= 'utf-8') as f:
                valid_hard = [word.strip().upper() for word in f.readlines()]
            with open('English (EZ dataset).txt', 'r', encoding= 'utf-8') as f:
                valid_ez = [word.strip().upper() for word in f.readlines()]
            
            self.solutions = data
            self.valid_guesses = set(valid_hard + valid_ez)

        elif self.mode == 'MATH':
            # Load các biểu thức từ file toán học
            with open('math_dataset.txt', 'r') as inp:
                self.solutions = [line.strip().upper() for line in inp.readlines()]
            self.valid_guesses = set(self.solutions)
    
    # Hàm reset game để bắt đầu ván mới hoặc load ván cũ
    def reset_game(self):
        self.ans = random.choice(self.solutions).upper()
        self.guesses = []       
        self.current_guess = ""  
        self.result = ""         
        self.hint_used = 0
        self.history_stack = Stack() # Tạo Stack() mới rỗng
        self.reset_key_color()

    # Hàm trả lại bảng gốc của bàn phím
    def reset_key_color(self):
        """
        Khởi tạo Dictionary lưu màu sắc của từng phím
        Key: Ký tự (A, B, C...), Value: Màu sắc (Gray, Green, Yellow)
        Khi người chơi kết thúc game hoặc tạo ván game mới
        --> Hàm này giúp reset màu của bàn phím ảo về màu viền mặc định là 'outline'
        """
        self.key_colors = {}
        if self.mode == "WORD":
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        else:
            chars = "0123456789+-*/="
        for char in chars:
            self.key_colors[char] = outline

    # Hàm kiểm tra đoán và cập nhật màu sắc cho từng chữ cái 
    # --> Thuật toán kiểm tra chính của game
    def check_guess(self, guess):
        """
        So sánh từ người chơi nhập (guess) với đáp án (ans).
        Logic 2 vòng lặp:
        - Vòng 1: Tìm màu XANH (Đúng ký tự, đúng vị trí).
        - Vòng 2: Tìm màu VÀNG (Đúng ký tự, sai vị trí) và XÁM (Sai).
        """
        
        result_colors = [gray]*5    # Mặc định là phím ảo màu xám
        ans_letter = list(self.ans) # Tạo danh sách các kí tự có trong đáp án

        # Vòng 1: Tìm màu XANH (từ đúng vị trí)
        for i in range(5):
            if guess[i] == self.ans[i]:
                result_colors[i] = green
                ans_letter[i] = None                # Đánh dấu từ ở vị trí này đã xử lí và loại bỏ để không xử lí tiếp trong vòng 2
                self.key_colors[guess[i]] = green   # Cập nhật bàn phím
            
        # Vòng 2: Tìm màu VÀNG và XÁM
        for i in range(5):
            if result_colors[i] != green:       # Chỉ xét những ô chưa xanh
                if guess[i] in ans_letter:
                    result_colors[i] = yellow
                    ans_letter.remove(guess[i]) # Xóa một kí tự trong đáp án để tránh duplicate màu vàng

                    # Chỉ cập nhật bàn phím thành vàng nếu nó chưa phải là xanh
                    if self.key_colors[guess[i]] != green:
                        self.key_colors[guess[i]] = yellow
                
                # Nếu không xanh, không vàng --> xám
                elif self.key_colors[guess[i]] != green and self.key_colors[guess[i]] != yellow:
                    self.key_colors[guess[i]] = gray

        return result_colors
    
    # Hàm xử lý khi người chơi nhấn phím enter (submit)
    def submit_guess(self):
        # Điều kiện: phải đủ 5 kí tự và chưa hết 6 lượt đoán
        if len(self.current_guess) == 5 and len(self.guesses) < 6:

            # Kiểm tra từ có hợp lệ (có trong từ điển) hay không
            if self.current_guess in self.valid_guesses:

                self.guesses.append(self.current_guess)
                self.history_stack.push(self.current_guess) # Đẩy vào Stack để lưu lịch sử

                # Dùng hàm check_guess() để kiểm tra
                self.check_guess(self.current_guess)

                if self.current_guess == self.ans:
                    self.result = "w"   # Thắng
                elif len(self.guesses) == 6:
                    self.result = "l"   # Thua
                
                self.current_guess = "" # Reset ô nhập chữ
            else:
                # Nếu từ không có trong từ điển thì báo lỗi
                return "invalid_word"
    
    # Hàm xử lý khi người chơi muốn undo lần đoán cuối cùng
    def undo_guess(self):
        """
        Hàm sử dụng STACK để quay lui trạng thái.
        Khi Undo, ta phải tính toán lại màu sắc bàn phím dựa trên các từ còn lại.
        """

        # Chỉ được undo khi game chưa kết thúc và Stack không rỗng
        if self.result == "" and not self.history_stack.is_empty():
            removed_word = self.history_stack.pop() #Lấy từ vừa đoán ra khỏi Stack
            
            if len(self.guesses) > 0:
                self.guesses.pop()  # Xóa khỏi danh sách hiển thị
            
            # Sau khi xóa xong phải reset lại màu của bàn phíma ảo
            self.reset_key_color()
            for guess in self.guesses:
                self.check_guess(guess)
            return True
        return False
    
    # Hàm xử lí khi nhập chữ cái vào từ đang gõ
    def add_letter(self, letter):
        if len(self.current_guess) < 5 and self.result == "":
            self.current_guess += letter

    # Hàm xử lí khi xóa chữ cái cuối cùng của từ đang gõ
    def remove_letter(self):
        if len(self.current_guess) > 0 and self.result == "":
            self.current_guess = self.current_guess[:-1]

    # Hàm cung cấp gợi ý cho người chơi
    def get_hint(self):
        """
        Hàm trả về một ký tự bất kì chưa được đoán đúng để gợi ý cho người chơi.
        """
        available_indices = [0, 1, 2, 3, 4]

        # Loại bỏ các vị trí mà người chơi đã đoán đúng (hiện màu xanh)
        for guess in self.guesses:
            for i in range(5):
                if guess[i] == self.ans[i] and i in available_indices:
                    available_indices.remove(i)

        # Nếu đã đoán đúng hết và hoặc không còn gì để gợi ý thì trả về None
        if not available_indices:
            return None  # No more hints available
        
        # Chọn random một vị trí
        idx = random.choice(available_indices)
        self.hint_used += 1
        return idx, self.ans[idx]
    
    #--- Các hàm liên quan đến Save/Load dữ liệu người chơi (Giao tiếp với file resume.py)

    # Hàm kiểm tra xem có dữ liệu lưu của người chơi hay không
    def check_has_save(self, username):
        return resume.check_name_exist(username)
    
    # Hàm lưu trạng thái hiện tại của game vào file last_play.txt
    def save_state(self, username, time_played):
        resume.save_last_play(username, self.ans, self.guesses, self.hint_used, time_played)

    # Hàm tải trạng thái đã lưu của game từ file last_play.txt
    def load_state(self, username):
        """
        Khôi phục toàn bộ trạng thái game từ file save.
        Quy trình: Load dữ liệu -> Khôi phục biến -> Khôi phục Stack -> Tính lại màu sắc.
        """
        data = resume.load_last_play(username)

        if not data:
            return None
        
        _, saved_ans, saved_guesses, saved_hint, saved_time = data

        # Kiểm tra lại chế độ chơi của save game thông qua đáp án của ván game đó
        if any(char in "1234567890+-=*/" for char in saved_ans):
            self.mode = 'MATH'
        else:
            self.mode = 'WORD'
        
        # Load lại từ điển theo chế độ chơi đó
        self.load_data()

        # Khôi phục các biến cơ bản
        self.ans = saved_ans
        self.guesses = saved_guesses
        self.hint_used = saved_hint
        self.result = ""

        # Khôi phục Stack lịch sử cũ (để có thể undo khi load lại game)
        self.history_stack = Stack()
        for guess in self.guesses:
            self.history_stack.push(guess)

        # Khôi phục màu bàn phím
        self.reset_key_color()
        for guess in self.guesses:
            self.check_guess(guess)

        return saved_time   # Trả về thời gian mà người này đã chơi, dữ liệu dùng để tính toán trong file main.py