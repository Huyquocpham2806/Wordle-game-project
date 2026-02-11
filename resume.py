from security import xor_string
file = "last_play.txt"

# Hàm lấy dữ liệu
def get_data():
    """
    Hàm dùng để lấy dữ liệu từ file last_play.txt.
    Vì dữ liệu trong file đang bị mã hóa (XOR), nên cần giải mã ra text thường
    để các hàm khác có thể xử lý được.
    """
    try: 
        with open(file, 'r', encoding='utf-8') as inp:
            lines = inp.readlines()

        # Giải mã bằng hàm xor_string() 
        decodedline = [xor_string(line.strip()) for line in lines]
        return decodedline
    # Nếu không kiếm thấy file thì tự động tạo file mới và trả về danh sách rỗng
    except FileNotFoundError:
        with open('last_play.txt', 'w', encoding= 'utf-8') as f:
            pass
        return []

# Hàm lưu dữ liệu
def save_last_play(username, ans, guesses, hint_used, time_played):
    """
    Hàm dùng để lưu trạng thái game hiện tại của người chơi.
    Các bước thực hiện:
    Đọc dữ liệu cũ -> Tìm dòng của user -> Ghi đè dòng đó (hoặc thêm mới) -> Mã hóa -> Ghi xuống file.
    """
    lines = get_data() # Dữ liệu ở dạng text thường
    new_lines = []
    found = False

    # Danh sách các từ mà người chơi đã đoán được ghi lại
    # Sau đó được chuyển thành list, ngăn cách nhau bởi dấu phẩy
    guesses_str = ','.join(guesses)

    # Lưu dữ liệu dưới dạng format chuẩn:
    # tên|đáp án của ván chơi|những từ người chơi đã đoán|số lượt gợi ý đã dùng|thời gian đã chơi
    raw_data = f'{username}|{ans}|{guesses_str}|{hint_used}|{time_played}'

    # Duyệt qua danh sách cũ để tìm tên người chơi
    for line in lines:
        parts = line.strip().split('|')
        if parts[0] == username:
            # Nếu tìm thấy thì thay thế bằng dữ liệu mới
            new_lines.append(raw_data)
            found = True
        else:
            # Nếu khong phải user này thì giữ nguyên thông tin cũ
            new_lines.append(line)

    # Nếu user mới hoàn toàn thì thêm vào cuối
    if not found:
        new_lines.append(raw_data)

    # Ghi lại toàn bộ danh sách mới và được mã hóa
    with open(file, 'w', encoding='utf-8') as out:
        for line in new_lines:
            encodedline = xor_string(line)
            out.write(encodedline + "\n")

# Hàm tải dữ liệu cũ của người chơi
def load_last_play(username):
    """
    Hàm dùng dể tìm kiếm và trả về dữ liệu save game của user
    Trả về: (tên, đáp án của game, các từ đã đoán, số gợi ý, thời gian)
    """
    lines = get_data()
    for line in lines:
        # Tự động bỏ qua nếu như gặp phải dòng trống
        if not line.strip():
            continue
        
        part = line.strip().split("|")

        # Kiểm tra user và đủ 5 trường dữ liệu
        if len(part) >= 5 and part[0] == username:
            ans = part[1]
            guesses_str = part[2]

            # chuyển Các từ đã đoán về ngược lại list
            # VD: "APPLE, ONION" -> ["APPLE", "ONION"]
            if len(guesses_str) > 0:
                guesses = guesses_str.split(",")
            else:
                guesses = [] # Nếu chưa đoán từ nào thì trả về danh sách rỗng

            hint_uses = int(part[3])
            time_played = float(part[4])

            return username, ans, guesses, hint_uses, time_played 
    
    return None # Trả về None khi khônng tìm thấy dữ liệu của người chơi

# Hàm xóa dữ liệu cũ của người chơi
def delete_last_play(username):
    """
    Hàm dùng để xóa dòng dữ liệu save của user khỏi file.
    Khi người chơi hoàn thành game hoặc chọn chơi mới từ đầu thì dữ liệu save không cần dùng tới nữa
    -> xóa đi để dễ quản lí
    """
    lines = get_data()
    new_lines = []
    
    # Duyệt quả file cũ để dữ lại các user không cần xóa
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) > 0 and parts[0] != username:
            new_lines.append(line)
    
    # Mã hóa và ghi ngược lại xuống file
    with open(file, 'w', encoding = 'utf-8') as out:
        for line in new_lines:
            encodedline = xor_string(line.strip())
            out.write(encodedline + "\n")

# Hàm kiểm tra tên người chơi đã tồn tại hay chưa
def check_name_exist(username):
    """
    Hàm dùng để kiểm tra xem user có save game đang dang dở không.
    Trong game_logic có một tính năng là kiểm tra xem người chơi có TỪNG save game hay không
    - Nếu có, game sẽ thực hiện vẽ nút RESUME
    - Nếu không, hỏi thẳng người chơi muốn chọn chế MATH/WORD
    """

    lines = get_data()
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) > 0 and parts[0] == username:
            return True
    return False
