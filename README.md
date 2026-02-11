# Đồ án: Trò chơi Đoán từ (Wordle)

**Môn học:** Cơ sở lập trình cho Trí tuệ nhân tạo  
**Sinh viên thực hiện:** Phạm Trường Quốc Huy  
**MSSV:** 25122071  
**Lớp:** 25TNT2  

---

## 1. Giới thiệu

Đây là phần mềm mô phỏng trò chơi đoán từ (**Wordle**) và biến thể đoán biểu thức toán học (**Nerdle**). Dự án được xây dựng hoàn toàn bằng ngôn ngữ **Python** với giao diện đồ họa sử dụng thư viện **Pygame**.

Dự án tập trung vào việc áp dụng các kiến thức nền tảng như quản lý tập tin, xử lý chuỗi, và đặc biệt là **tự cài đặt các cấu trúc dữ liệu (Data Structures)** thay vì sử dụng thư viện có sẵn, nhằm đáp ứng yêu của môn học.

### Lời ngỏ
Đây là dự án đầu tay nên chắc chắn không tránh khỏi những thiếu sót. Em rất mong nhận được những nhận xét và góp ý từ Thầy để hoàn thiện hơn tư duy lập trình của mình. Mọi ý kiến đóng góp xin gửi về email: [2512207195@student.hcmus.edu.vn]

**Ghi chú về AI:** Trong quá trình thực hiện, em có sử dụng AI làm công cụ hỗ trợ học tập để:
* Tiếp cận nhanh thư viện **Pygame** (do chưa từng sử dụng trước đây).
* Tham khảo nguyên lý thuật toán mã hóa **XOR**.
* Gợi ý cách tổ chức cấu trúc thư mục (clean architecture) và phương pháp kiểm thử (testing).
* *Toàn bộ mã nguồn logic và cấu trúc dữ liệu đều do em tự cài đặt và kiểm soát.*

---

## 2. Cấu trúc thư mục 

Cấu trúc mã nguồn trong thư mục `Resources`:

* **`main.py`**: Entry point của chương trình, quản lý vòng lặp chính (Game Loop) và điều hướng các trạng thái (State Machine).
* **`game_logic.py`**: Chứa class `WordleGame` xử lý logic cốt lõi (kiểm tra từ, so khớp màu sắc, quản lý lượt chơi) cho cả 2 chế độ Math và Word.
* **`ui.py`**: Quản lý toàn bộ việc vẽ giao diện (Render), các popup, bảng, và hiệu ứng hình ảnh.
* **`score_manager.py`**: Quản lý hệ thống người chơi, đăng nhập/đăng ký và bảng xếp hạng (Leaderboard). **(Sử dụng Linked List tự cài đặt)**.
* **`resume.py`**: Xử lý lưu/tải trạng thái game (Save/Load game).
* **`security.py`**: Module mã hóa/giải mã dữ liệu save game và thông tin người dùng **(Sử dụng thuật toán XOR)**.
* **`settings.py`**: Chứa các hằng số cấu hình (Màu sắc, kích thước, FPS...).
* **`data/`**: Thư mục chứa tài nguyên (font chữ, file dữ liệu từ vựng `word.txt`, `math_dataset.txt`, file save...).

---

## 3. Hướng dẫn cài đặt và chạy

1.  Đảm bảo máy tính đã cài đặt **Python** (phiên bản 3.x trở lên).
2.  Cài đặt thư viện `pygame` (Thư viện ngoài duy nhất được sử dụng cho đồ họa):
    ```bash
    pip install pygame
    ```
3.  Di chuyển vào thư mục `Resources` và chạy lệnh:
    ```bash
    python main.py
    ```

---

## 4. Điểm nhấn kỹ thuật (Technical Highlights)

Theo yêu cầu của đồ án, em đã **tự cài đặt** các thành phần cốt lõi sau mà không phụ thuộc vào thư viện có sẵn:

### Cấu trúc dữ liệu:
* **Linked List (Danh sách liên kết):** Được cài đặt trong `score_manager.py` để quản lý danh sách người chơi và bảng xếp hạng Top-20. Giúp tối ưu hóa việc thêm node mới và sắp xếp lại danh sách.
* **Stack (Ngăn xếp):** Được cài đặt để xử lý tính năng **Undo (Hoàn tác)**, cho phép người chơi quay lại các bước đoán trước đó theo nguyên tắc LIFO.

### Thuật toán:
* **File Encryption (Mã hóa):** Dữ liệu người dùng và file save được mã hóa bằng thuật toán **XOR** kết hợp khóa riêng, ngăn chặn việc người dùng mở file text để gian lận điểm số.
* **Sorting:** Tự cài đặt thuật toán sắp xếp để hiển thị Top-20 người chơi có thời gian giải đố nhanh nhất trên Leaderboard.

---

## 5. Bảng tự đánh giá

Dưới đây là bảng tự đánh giá mức độ hoàn thành các chức năng:

| STT | Chức năng | Yêu cầu chi tiết | Hoàn thiện | Ghi chú |
| :-- | :--- | :--- | :---: | :--- |
| **1** | **Màn hình bắt đầu** | | **100%** | |
| 1.1 | New Game | Nhập tên, kiểm tra trùng lặp trong Top-20. | 100% | |
| 1.2 | Top-20 List | Hiển thị 20 người chơi xuất sắc nhất, sắp xếp tăng dần. | 100% | Sử dụng Linked List & Sorting. |
| 1.3 | Resume | Tải lại ván chưa hoàn thành. Nút mờ nếu không có save. | 100% | |
| **2** | **Chức năng chơi** | | **100%** | |
| 2.1 | Gameplay | Logic Wordle (Xanh, Vàng, Xám). | 100% | |
| 2.2 | Bàn phím ảo | Hiển thị màu sắc trạng thái phím. | 100% | |
| 2.3 | Chế độ chơi | Hỗ trợ 2 chế độ: **Word** và **Math**. | 100% | Tự động phát hiện chế độ khi Resume. |
| **3** | **Cài đặt (Settings)** | | **100%** | |
| 3.1 | Time Scoring | Tính thời gian chơi để xếp hạng. | 100% | Đồng hồ dừng khi tạm ngưng game. |
| 3.2 | Toggle Keyboard | Bật/Tắt bàn phím ảo. | 100% | |
| 3.3 | Infinite Mode | Chơi không giới hạn. | 100% | Tự reset sau khi thắng/thua. |
| **4** | **Chức năng mở rộng** | | **100%** | |
| 4.1 | Undo | Quay lại bước trước (dùng Stack). | 100% | Có áp dụng phạt thời gian. |
| 4.2 | Hint (Gợi ý) | Gợi ý chữ cái đúng. | 100% | Tính năng đề xuất thêm. |
| 4.3 | Bảo mật file | Mã hóa file save/user. | 100% | Chống gian lận bằng cách sửa file text. |
| 4.4 | Multi-Account | Lưu trạng thái Resume riêng cho từng user. | 100% | Mỗi user có file save riêng biệt. |
| 4.5 | Confirmation | Bảng xác nhận khi thoát/reset. | 100% | Tăng trải nghiệm người dùng (UX). |

---

## 6. Video Demo

*(Bạn có thể chèn link video demo tại đây hoặc để file video trong thư mục nộp bài)*