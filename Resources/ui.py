import pygame
from settings import *
import settings

# Lớp vẽ bàn phím ảo
class Keyboardrender:
    """
    Lớp vẽ bàn phím ảo
    Bàn phím ảo sẽ tự đổi màu (xanh/vàng/xám) dựa trên các từ người chơi đã đoán
    """
    def __init__(self, font):
        self.font = font

    def draw(self, screen, game_data):
        # Xác định layout bàn phím dựa trên chế độ chơi
        if game_data.mode == 'WORD':
            layout = qwerty
        else:
            layout = num_layout

        # Duyệt qua từng hàng phím để vẽ màu
        for i in range(len(layout)):
            row_chars = layout[i]

            # Tính độ rộng của cả hàng để căn giữa màn hình
            # Công thức tính: (số phím)*(chiều rộng phím) + khoảng cách giữa các phím
            row_width = len(row_chars)*(key_width + key_gap) - key_gap
            st_x = (WIDTH - row_width)//2 # tọa độ x bắt đầu vẽ
            y = keyboard_y_start + i*(key_height + key_gap) #(các thông số này được định nghĩa trong file settings.py)

            # Duyệt qua từng phím trong hàng
            for j in range(len(row_chars)):
                char = row_chars[j]
                x = st_x + j*(key_width + key_gap)
                rect = pygame.Rect(x, y, key_width, key_height)

                # Lấy màu của phím từ file game_logic.py
                # Nếu là từ đang đoán thì trả về màu của từ đó
                # Nếu chưa đụng tới thì trả về mặc định là outline
                bg_color = game_data.key_colors.get(char, outline)
                
                # Vẽ màu
                if bg_color == outline:
                    # Nếu chưa đoán: vẽ viền rỗng
                    pygame.draw.rect(screen, bg_color, rect, 4, border_radius = 4)
                else:
                    # Nếu đã có màu: tô màu phím đó 
                    pygame.draw.rect(screen, bg_color, rect, border_radius = 4)

                # Vẽ kí tự lên phím
                text_surf = self.font.render(char, True, black)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

# Lớp vẽ bảng chơi
class Boardrender:
    """
    Dùng để vẽ lưới 6x5 chứa các từ người chơi đoán
    """
    def __init__(self, font):
        self.font = font

    def draw(self, screen, game_data):
        # Duyệt qua 6 hàng (6 lượt đoán)
        for row in range(6):
            row_color = []

            # Nếu hàng này đã đoán rồi --> lấy danh màu kết quả sau khi check (xanh/vàng/xám)
            if row < len(game_data.guesses):
                row_color = game_data.check_guess(game_data.guesses[row])

            # Duyệt qua 5 cột, 5 kí tự
            for col in range(5):
                # Rect(x, y, width, height)
                #pygame.draw.rect(screen, color, rect, width, border radius)
                # Tính tọa độ x, y cho từng ô vuông
                x = margin_left + col*(box_size + gap)
                y = margin_top + row*(box_size + gap)
                rect = pygame.Rect(x, y, box_size, box_size)

                # Vẽ khung viền mặc định (màu trắng)
                pygame.draw.rect(screen, white, rect, 3, 10)

                # ---XỬ LÍ MÀU NỀN CỦA Ô---
                if row < len(game_data.guesses): 
                    # Hàng cũ: tô màu theo kết quả check_guess
                    cell_color = row_color[col]
                    pygame.draw.rect(screen, cell_color, rect, border_radius = 10)
                else: 
                    # vẽ màu của hàng hiện tại
                    color = outline
                    # Thêm hiệu ứng viền sáng lên khi đang gõ, viền màu hồng (pink)
                    if row == len(game_data.guesses) and col < len(game_data.current_guess):
                        color = pink
                    pygame.draw.rect(screen, color, rect, 2, border_radius=10)

                # ---VẼ KÍ TỰ---
                char = None
                if row < len(game_data.guesses): # vẽ các từ trong quá khứ
                    char = game_data.guesses[row][col] 
                elif row == len(game_data.guesses): # vẽ các từ ở hiện tại
                    if col < len(game_data.current_guess):
                        char = game_data.current_guess[col]

                if char:
                    text_surface = self.font.render(char, True, black)
                    text_rect = text_surface.get_rect(center=rect.center)
                    #screen.blit(source(từ đâu), dest(vào đâu)): dán hình ảnh từ source vào dest
                    screen.blit(text_surface, text_rect)

# Lớp vẽ các popup (kết quả, cảnh báo, form đăng nhập)
class Popuprender:
    """
    Chức năng chính: quản lí tất cả các menu, thông báo (popup)
    Gồm có: kết quả, login, register, leaderboard, help, mode selection,...
    """
    def __init__(self, font_res, font_warn):
        # Khai báo các font chữ với kích thước khác nhau
        self.font_title = pygame.font.Font('freesansbold.ttf', 50)
        self.font_grid = pygame.font.Font('freesansbold.ttf', 40)
        self.font_key = pygame.font.Font('freesansbold.ttf', 30)
        self.font_res = font_res
        self.font_warn = font_warn

        # Tạo lớp nền mờ để làm tối màn hình khi hiện popup 
        self.dim_surface = pygame.Surface((WIDTH, HEIGHT))
        self.dim_surface.fill(black)
        self.dim_surface.set_alpha(180) # Độ trong suốt

    # 1. Vẽ cảnh báo lỗi (VD: sai pass, từ không hợp lệ)
    def draw_warning(self, screen, warning_msg):
        screen.blit(self.dim_surface, (0, 0)) # phủ nền tối trước
        rect = pygame.Rect(175, 300, 250, 100)
        pygame.draw.rect(screen, white, rect, border_radius=4)

        warn_surf = self.font_warn.render(warning_msg, True, red)
        warn_rect = warn_surf.get_rect(center=rect.center) # Hiện ở trên đầu bảng
        screen.blit(warn_surf, warn_rect)

    # 2. Vẽ kết quả thắng thua 
    def draw_result(self, screen, result, ans):
        screen.blit(self.dim_surface, (0, 0))
        rect = pygame.Rect(150, 300, 300, 100)

        msg = "Press SPACE to play again"
        sub_msg = f"The answer is: {ans}" # Nếu thua thì hiện thêm đáp án đúng

        # Xác định màu sắc và nội dung dựa trên kết quả
        msg1 = ""
        color = gray
        if result == "w":
            msg1 = f"YOU WIN"
            color = green
        
        elif result == "l":
            msg1 = f"YOU LOSE"
            color = red

        pygame.draw.rect(screen, color, rect, border_radius=10)

        # Vẽ text kết quả
        if result == 'l':
            # Nếu thua, hiện thêm đáp án đúng
            text_surface2 = self.font_res.render(sub_msg, True, white)
            text_rect2 = text_surface2.get_rect(center=rect.center)
            screen.blit(text_surface2, text_rect2)

            text_surface1 = self.font_res.render(msg1, True, white)
            text_rect1 = text_surface1.get_rect(center=(rect.centerx, rect.centery - 30))
            screen.blit(text_surface1, text_rect1)

            text_surface = self.font_res.render(msg, True, white)
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + 30))
            screen.blit(text_surface, text_rect)

        else:
            # Nếu thắng, chỉ hiện "you win" là đủ
            text_surface1 = self.font_res.render(msg1, True, white)
            text_rect1 = text_surface1.get_rect(center=(rect.centerx, rect.centery - 20))
            screen.blit(text_surface1, text_rect1)

            text_surface = self.font_res.render(msg, True, white)
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + 20))
            screen.blit(text_surface, text_rect)

    # 3. Vẽ menu bắt đầu (register/login)
    def draw_start_menu(self, screen):
        screen.fill(beige)

        center_x = WIDTH//2
        title = self.font_title.render('WORDLE GAME', True, black)
        screen.blit(title, title.get_rect(center=(center_x, 200)))

        # Vẽ nút login
        btn_login = pygame.Rect(0, 0, 200, 60)
        btn_login.center = (center_x, 350)

        pygame.draw.rect(screen, green, btn_login, border_radius = 10)
        text_login = self.font_key.render('LOGIN', True, white)
        screen.blit(text_login, text_login.get_rect(center=btn_login.center))

        # Vẽ nút register
        btn_regis = pygame.Rect(0, 0, 200, 60)
        btn_regis.center = (center_x, 450)

        pygame.draw.rect(screen, yellow, btn_regis, border_radius = 10)
        text_regis = self.font_key.render('REGISTER', True, white)
        screen.blit(text_regis, text_regis.get_rect(center=btn_regis.center))

        return btn_login, btn_regis
    
    # 4. Vẽ form điền thông tin login/register
    def draw_logre_form(self, screen, name, password, active_field, err_msg="", title_text="LOGIN"):
        screen.fill(beige)

        # Vẽ bảng nền trắng
        center_x, center_y = WIDTH//2, HEIGHT//2
        panel_rect = pygame.Rect(0, 0, 450, 300)
        panel_rect.center = (center_x, center_y)

        pygame.draw.rect(screen, white, panel_rect, border_radius=15)

        title = self.font_res.render(title_text, True, black)
        screen.blit(title, title.get_rect(center=(center_x, center_y - 120)))

        # Vẽ ô nhập Name
        name_rect = pygame.Rect(0, 0, 300, 50)
        name_rect.center = (center_x, center_y - 40)
        if active_field == 0: # Nếu = 0 thì đang chọn vào ô này --> màu xanh, ngược lại thì màu xám
            color_name = green
        else:
            color_name = gray
        
        pygame.draw.rect(screen, color_name, name_rect, 3, border_radius=5)
        nm_surf = self.font_key.render(name, True, black)
        screen.blit(nm_surf, (name_rect.x + 10, name_rect.y + 10))

        lbl_name = self.font_res.render("Name", True, gray)
        screen.blit(lbl_name, (name_rect.x, name_rect.y - 25))

        # Vẽ ô nhập Pass
        pass_rect = pygame.Rect(0, 0, 300, 50)
        pass_rect.center = (center_x, center_y + 50)
        if active_field == 1: #Ngược lại so với ô name
            color_name = green
        else: 
            color_name = gray

        pygame.draw.rect(screen, color_name, pass_rect, 3, border_radius=5)
        hidden_pass = "*"*len(password) # che mật khẩu bằng dấu *
        ps_surf = self.font_key.render(hidden_pass, True, black)
        screen.blit(ps_surf, (pass_rect.x + 10, pass_rect.y + 10))

        lbl_pass = self.font_res.render("Password:", True, gray)
        screen.blit(lbl_pass, (pass_rect.x, pass_rect.y - 25))

        # Hiện thông báo lỗi
        if err_msg:
            err_surf = self.font_res.render(err_msg, True, red)
            screen.blit(err_surf, err_surf.get_rect(center= (center_x, center_y + 100)))

        # Vẽ một nút nhỏ màu xám
        btn_back = pygame.Rect(panel_rect.right - 75, panel_rect.y + 15, 60, 30)
        pygame.draw.rect(screen, light_gray, btn_back, border_radius=5)
        
        # Vẽ kí hiệu <--Back
        txt_back = self.font_res.render("<-", True, black)
        screen.blit(txt_back, txt_back.get_rect(center=btn_back.center))

        return name_rect, pass_rect, btn_back

    # 5. Vẽ bảng xếp hạng
    def draw_leaderboard(self, screen, scores):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2
        rect = pygame.Rect(0, 0, 500, 700)
        rect.center = (center_x, center_y)

        pygame.draw.rect(screen, white, rect, border_radius = 10)
        pygame.draw.rect(screen, yellow, rect, 4, border_radius = 10)

        title = self.font_grid.render("LEADERBOARD", True, yellow)
        screen.blit(title, title.get_rect(center= (center_x, rect.y + 50)))

        pygame.draw.line(screen, gray, (rect.x + 50, rect.y + 80), (rect.right - 50, rect.y + 80), 2)

        start_y = rect.y + 100

        if not scores:
            err_msg = self.font_warn.render("No records yet", True, red)
            screen.blit(err_msg, err_msg.get_rect(center= (center_x, center_y)))
        else:
            for i, entry in enumerate(scores):
                # tô màu cho top 1, 2, 3
                if i == 0:
                    color = red
                elif i < 3:
                    color = green
                else:
                    color = gray
                rank_name = f"{i+1}. {entry['name']}"
                score_text = f"{entry['score']}s"

                name_surf = self.font_res.render(rank_name, True, color)
                screen.blit(name_surf, (rect.x + 60, start_y + i*30))

                score_surf = self.font_res.render(score_text, True, color)
                screen.blit(score_surf, score_surf.get_rect(topright=(rect.right - 40, start_y + i*30)))

    # 6. Vẽ hướng dẫn chơi 
    def draw_help(self, screen, game_logic):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2

        panel_surf = pygame.Rect(0, 0, 560, 700)
        panel_surf.center = (center_x, center_y)
        pygame.draw.rect(screen, white, panel_surf, border_radius = 10)
        pygame.draw.rect(screen, green, panel_surf, 4, border_radius = 10)

        title = self.font_title.render("HOW TO PLAY", True, green)
        screen.blit(title, title.get_rect(center= (center_x, panel_surf.y + 40)))

        # Nếu chế độ đang ở WORD thì nội dung khác
        if game_logic.mode == "WORD":
            lines = [
                "You have to guess the hidden WORD in 6 tries",
                "and the color of the letters changes to show",
                "how close you are.",
                "* GREEN: Correct letter & spot",
                "* YELLOW: Correct letter, wrong spot",
                "* GRAY: Letter not in word",
                "--------------------------------------------------------------",
                "SCORING RULE:",
                "Rank is based on AVERAGE TIME per win.",  
                "The FASTER you solve, the higher your rank!", 
                "* HINT: +15 seconds to your timer", 
                "* UNDO: +30 seconds to your timer",
                "--------------------------------------------------------------",
                "       Solve fast to top the Leaderboard!      "
            ]
        else: # ở MATH thì khác một chút
            lines = [
                "You have to guess the hidden EQUATION in 6 tries",
                "and the color of the letters changes to show",
                "how close you are.",
                "* GREEN: Correct number/sign & spot",
                "* YELLOW: Correct number, wrong spot",
                "* GRAY: Letter not in equation",
                "--------------------------------------------------------------",
                "SCORING RULE:",
                "Rank is based on AVERAGE TIME per win.",  
                "The FASTER you solve, the higher your rank!", 
                "* HINT: +15 seconds to your timer", 
                "* UNDO: +30 seconds to your timer",
                "--------------------------------------------------------------",
                "       Solve fast to top the Leaderboard!      "
            ]

        start_y = panel_surf.y + 90
        for i, line in enumerate(lines):
            color = black
            if "GREEN" in line:
                color = green
            elif "YELLOW" in line:
                color = yellow
            elif "GRAY" in line:
                color = gray
            elif "Good" in line:
                color = red

            text = self.font_res.render(line, True, color)
            screen.blit(text, (panel_surf.x + 20, start_y + i*40))

    # 7. Vẽ menu hỏi RESUME
    def draw_resume_menu(self, screen, username):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2
        rect = pygame.Rect(0, 0, 450, 250)
        rect.center = (center_x, center_y)

        pygame.draw.rect(screen, white, rect, border_radius= 15)
        pygame.draw.rect(screen, gray, rect, 3, border_radius = 15)

        msg1 = self.font_title.render(f'Hi, {username}!', True, black)
        screen.blit(msg1, msg1.get_rect(center = (center_x, rect.y + 50)))

        msg2 = self.font_res.render(f'You have an unfinished game', True, black)
        screen.blit(msg2, msg2.get_rect(center = (center_x, rect.y + 90)))

        btn_resume = pygame.Rect(0, 0, 160, 50)
        btn_resume.center = (center_x - 90, rect.y + 170)
        pygame.draw.rect(screen, orange, btn_resume, border_radius=10)

        text_surf = self.font_res.render('RESUME', True, black)
        screen.blit(text_surf, text_surf.get_rect(center= btn_resume.center))

        btn_new = pygame.Rect(0, 0, 160, 50)
        btn_new.center = (center_x +90, rect.y + 170)
        pygame.draw.rect(screen, green, btn_new, border_radius=10)

        new_surf = self.font_res.render('NEW', True, black)
        screen.blit(new_surf, new_surf.get_rect(center= btn_new.center))

        return btn_resume, btn_new

    # 8. Vẽ menu chọn chế độ 
    def draw_mode_selection(self, screen):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2
        rect = pygame.Rect(0, 0, 500, 500)
        rect.center = (center_x, center_y)

        rect.y = 30
        pygame.draw.rect(screen, white, rect, border_radius = 15)
        pygame.draw.rect(screen, gray, rect, 3, border_radius = 15)

        title = self.font_title.render('SELECT MODE', True, black)
        screen.blit(title, title.get_rect(center= (center_x, rect.y + 80)))
        
        # Nút MATH
        btn_math = pygame.Rect(0, 0, 180, 60)
        btn_math.center = (center_x - 100, rect.y + 250)
        pygame.draw.rect(screen, orange, btn_math, border_radius=10)
        txt_math = self.font_key.render("MATH", True, white)
        screen.blit(txt_math, txt_math.get_rect(center=btn_math.center))

        # Nút WORD
        btn_word = pygame.Rect(0, 0, 180, 60)
        btn_word.center = (center_x + 100, rect.y + 250)
        pygame.draw.rect(screen, green, btn_word, border_radius=10)
        txt_word = self.font_key.render("WORD", True, white)
        screen.blit(txt_word, txt_word.get_rect(center=btn_word.center))

        return btn_math, btn_word
    
    # 9. Vẽ menu chọn độ khó (đối với WORD)
    def draw_difficulty_selection(self, screen):
        screen.blit(self.dim_surface, (0, 0))
        center_x, center_y = WIDTH//2, HEIGHT//2
        
        rect = pygame.Rect(0, 0, 500, 500)
        rect.center = (center_x, center_y)

        rect.y = 30
        pygame.draw.rect(screen, white, rect, border_radius=15)
        pygame.draw.rect(screen, gray, rect, 3, border_radius=15)
        
        title = self.font_title.render("DIFFICULTY", True, black)
        screen.blit(title, title.get_rect(center=(center_x, rect.y + 80)))

        # Nút EASY
        btn_easy = pygame.Rect(0, 0, 180, 60)
        btn_easy.center = (center_x - 100, rect.y + 250)
        pygame.draw.rect(screen, yellow, btn_easy, border_radius=10)
        txt_easy = self.font_key.render("EASY", True, black) 
        screen.blit(txt_easy, txt_easy.get_rect(center=btn_easy.center))

        # Nút HARD
        btn_hard = pygame.Rect(0, 0, 180, 60)
        btn_hard.center = (center_x + 100, rect.y + 250)
        pygame.draw.rect(screen, red, btn_hard, border_radius=10)
        txt_hard = self.font_key.render("HARD", True, white)
        screen.blit(txt_hard, txt_hard.get_rect(center=btn_hard.center))

        return btn_easy, btn_hard

    # 10. Vẽ menu xác thực rest
    def draw_confirm_menu(self, screen):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2
        rect = pygame.Rect(0, 0, 500, 300)
        rect.center = (center_x, center_y)

        rect.y = 30
        pygame.draw.rect(screen, white, rect, border_radius=15)
        pygame.draw.rect(screen, gray, rect, 3, border_radius=15)

        title = self.font_key.render("QUIT TO MENU?", True, black)
        screen.blit(title, title.get_rect(center= (center_x, rect.y + 80)))

        sub = self.font_res.render("Progress will be LOST", True, black)
        screen.blit(sub, sub.get_rect(center= (center_x, rect.y + 110)))

        # Nút YES (Màu xanh)
        btn_yes = pygame.Rect(0, 0, 100, 50)
        btn_yes.center = (center_x - 70, rect.y + 180)
        pygame.draw.rect(screen, green, btn_yes, border_radius=10)
        txt_yes = self.font_res.render("YES", True, white)
        screen.blit(txt_yes, txt_yes.get_rect(center=btn_yes.center))

        # Nút NO (Màu đỏ/xám)
        btn_no = pygame.Rect(0, 0, 100, 50)
        btn_no.center = (center_x + 70, rect.y + 180)
        pygame.draw.rect(screen, red, btn_no, border_radius=10)
        txt_no = self.font_res.render("NO", True, white)
        screen.blit(txt_no, txt_no.get_rect(center=btn_no.center))

        return btn_yes, btn_no
    
    # 11. Vẽ menu khi chọn home
    def draw_home_option(self, screen):
        screen.blit(self.dim_surface, (0, 0))

        center_x, center_y = WIDTH//2, HEIGHT//2
        rect = pygame.Rect(0, 0, 500, 300)
        rect.center = (center_x, center_y)

        rect.y = 30
        pygame.draw.rect(screen, white, rect, border_radius=15)
        pygame.draw.rect(screen, gray, rect, 3, border_radius=15)

        # Tiêu đề
        title = self.font_key.render("PAUSED", True, black)
        screen.blit(title, title.get_rect(center=(center_x, rect.y + 40)))

        # Nút QUIT (Về chọn chế độ)
        btn_quit_level = pygame.Rect(0, 0, 200, 50)
        btn_quit_level.center = (center_x, rect.y + 100)
        pygame.draw.rect(screen, orange, btn_quit_level, border_radius=10)
        
        txt_quit = self.font_res.render("Quit", True, white)
        screen.blit(txt_quit, txt_quit.get_rect(center=btn_quit_level.center))

        # Nút LOG OUT
        btn_logout = pygame.Rect(0, 0, 200, 50)
        btn_logout.center = (center_x, rect.y + 160)
        pygame.draw.rect(screen, red, btn_logout, border_radius=10)
        
        txt_logout = self.font_res.render("Log Out", True, white)
        screen.blit(txt_logout, txt_logout.get_rect(center=btn_logout.center))

        # Trả về 2 nút để xử lý bấm chuột
        return btn_quit_level, btn_logout    

# Lớp chính quản lý giao diện, gọi các lớp con để vẽ từng phần của giao diện
class WordleUI:
    def __init__(self, screen):
        self.screen = screen

        # Khai báo các font chữ
        self.font_title = pygame.font.Font('freesansbold.ttf', 50)
        self.font_grid = pygame.font.Font('freesansbold.ttf', 40)
        self.font_key = pygame.font.Font('freesansbold.ttf', 30)
        self.font_res = pygame.font.Font('freesansbold.ttf', 20)
        self.font_warn = pygame.font.Font('freesansbold.ttf', 25)
        
        # Khởi tạo các module vẽ con 
        # Liên kết với các lớp phía trên để dễ quản lí 
        self.board_renderer = Boardrender(self.font_grid)
        self.keyboard_renderer = Keyboardrender(self.font_key)
        self.popup_renderer = Popuprender(self.font_res, self.font_warn)
    
    def draw(self, game_logic, warn_msg = "", show_res = False, seconds = 0):
        # Tô màu nền trước
        self.screen.fill(beige)
        
        # 1. Vẽ Title
        if game_logic.mode == "WORD":
            title = 'WORDLE'
        else:
            title = 'NERDLE'
        title_game = self.font_title.render(title, True, black)
        self.screen.blit(title_game, title_game.get_rect(center=(WIDTH//2, 50)))
        pygame.draw.line(self.screen, gray, (0, 85), (WIDTH, 85), 1)
        
        # 2. Gọi các bộ phận con làm việc (Vẽ lưới + bàn phím)
        self.board_renderer.draw(self.screen, game_logic)
        if settings.show_keyboard:
            self.keyboard_renderer.draw(self.screen, game_logic)
        
        # 3. Vẽ Popup hiện thông báo lỗi nếu cần
        if warn_msg:
            self.popup_renderer.draw_warning(self.screen, warn_msg)
        elif show_res:
            self.popup_renderer.draw_result(self.screen, game_logic.result, game_logic.ans)

        # 4. Vẽ nút gợi ý
        btn_hint_rect = pygame.Rect(120, 40, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_hint_rect, border_radius=10)
        # Vẽ icon bóng đèn 
        cx, cy= btn_hint_rect.centerx, btn_hint_rect.centery
        pygame.draw.circle(self.screen, dark_green, (cx, cy - 5), 12, 2)
        pygame.draw.rect(self.screen, dark_green, (cx - 6, cy + 6, 12, 9))
        pygame.draw.line(self.screen, dark_green, (cx - 4, cy + 8), (cx + 4, cy+ 8), 1)
        pygame.draw.line(self.screen, dark_green, (cx - 4, cy + 11), (cx + 4, cy + 11), 1)

        # Vẽ số lượt gợi ý đã dùng
        if game_logic.hint_used > 0:
            hint_penalty_text = self.font_res.render(f'{game_logic.hint_used}', True, red)
            hint_pen_surf = pygame.draw.circle(self.screen, yellow, (btn_hint_rect.right, btn_hint_rect.top), 12) 
            self.screen.blit(hint_penalty_text, hint_penalty_text.get_rect(center= hint_pen_surf.center))

        # 5. Vẽ nút hướng dẫn
        btn_help_cir = pygame.Rect(20, 40, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_help_cir, border_radius= 10)
        # Vẽ dấu chấm hỏi
        q_mark = self.font_res.render('?', True, dark_green)
        self.screen.blit(q_mark, q_mark.get_rect(center=btn_help_cir.center))

        # 6. Vẽ nút hiện bản xếp hạng
        btn_rank_cir = pygame.Rect(70, 40, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_rank_cir, border_radius=10)
        # Vẽ biểu tượng cột xếp hạng
        pygame.draw.rect(self.screen, dark_green, (btn_rank_cir.centerx - 8, btn_rank_cir.centery + 2, 4, 8))
        pygame.draw.rect(self.screen, dark_green, (btn_rank_cir.centerx - 2, btn_rank_cir.centery - 6 , 4, 16))
        pygame.draw.rect(self.screen, dark_green, (btn_rank_cir.centerx + 4, btn_rank_cir.centery - 2, 4, 12))

        # 7. Vẽ đồng hồ
        seconds = int(seconds)
        mins = seconds//60
        secs = seconds%60
        time_str = f'{mins:02}:{secs:02}'

        time_rect = pygame.Rect(WIDTH - 120, 40, 100, 40)
        pygame.draw.rect(self.screen, light_gray, time_rect, border_radius=10)

        time_surf = self.font_key.render(time_str, True, dark_green)
        self.screen.blit(time_surf,  time_surf.get_rect(center=time_rect.center))

        # 8. Vẽ nút undo
        btn_undo_rect = pygame.Rect(WIDTH - 170, 40, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_undo_rect, border_radius=10)
        # Vẽ mũi tên quay lại 
        cx, cy = btn_undo_rect.centerx, btn_undo_rect.centery
        pygame.draw.polygon(self.screen, dark_green, [(cx - 5, cy), (cx + 2, cy - 6), (cx + 2, cy + 6)])
        pygame.draw.rect(self.screen, dark_green, (cx + 2, cy - 2, 6, 4))

        # 9. Vẽ nút bật tắt bàn phím ảo
        btn_settings_rect = pygame.Rect(20, 90, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_settings_rect, border_radius=10)
        pygame.draw.circle(self.screen, dark_green, (btn_settings_rect.centerx, btn_settings_rect.centery), 12, 2)
        pygame.draw.circle(self.screen, dark_green, (btn_settings_rect.centerx, btn_settings_rect.centery), 6, 2)

        # 10. Vẽ nút home
        btn_home_rect = pygame.Rect(WIDTH - 60, 90, 40, 40)
        pygame.draw.rect(self.screen, light_gray, btn_home_rect, border_radius= 10)

        # Vẽ ngôi nhà
        cx, cy = btn_home_rect.centerx, btn_home_rect.centery
        pygame.draw.polygon(self.screen, dark_green, [(cx, cy - 8), (cx - 8, cy - 2), (cx + 8, cy - 2)])
        pygame.draw.rect(self.screen, dark_green, (cx - 6, cy -2, 12, 10))
        pygame.draw.rect(self.screen, white, (cx -2, cy + 2, 4, 6))


        # Trả về các Rect (kích thước) của nút bấm để xử lí sự kiện Click ở file main.py 
        return btn_hint_rect, btn_help_cir, btn_rank_cir, btn_undo_rect, btn_settings_rect, btn_home_rect
