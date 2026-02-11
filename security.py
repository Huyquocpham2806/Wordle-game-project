# Ở phần thuật toán mã hóa thì được tham khảo và hỗ trợ từ AI
# AI giúp gợi ý thuật toán dễ sử dụng và hiệu quả trong việc bảo mật
# Đồng thời nó cũng miêu tả cách thuật toán hoạt động

XorKey = 286
# Là số nguyên bất kì, được dùng để mã hóa và giải mã dữ liệu
# Nếu quá trình mã hóa và giải mã dùng khác số này thì toàn bộ file save cũ sẽ không đọc được nữa

def xor_string(text):
    """
    Hàm thực hiện thuật toán mã hóa XOR
    
    Nguyên lí hoạt động:
    Thuật toán này dựa trên tính chất đặc biệt của toán tử Bitwise XOR (^):
    
        (A ^ Key) ^ Key = A
    
    Điều này có nghĩa là:
    - Nếu ta lấy một ký tự (A) XOR với Key, ta được ký tự mã hóa (B) --> Encoding
    - Nếu ta lấy ký tự mã hóa (B) XOR lại với Key lần nữa, ta được ký tự gốc (A) --> Decoding
    
    => Hàm này vừa đóng vai trò mã hóa và giải mã
    """
    res = ""
    for char in text:
        # Input: hàm nhận đầu vào là một text thường

        # ord(char): chuyển từng kí tự trong A thành mã số nguyên trong Unicode
        # (^ XorKey): Thực hiện phép toán XOR giữa mã Unicode và Key
        # chr(): Chuyển kết ủa vừa tính được ngược lại thành kí tự

        # Output: ghép từng kí tự mới vào chuỗi kết quả và in ra
        res += chr(ord(char) ^ XorKey)
    return res