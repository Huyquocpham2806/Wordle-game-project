import pygame
import resume
from settings import *  # import các hằng số kích thước từ module settings
from game_logic import WordleGame
import settings         # phải imprt dòng này để import thêm biến show_keyboard
from ui import WordleUI
from score_manager import ScoreManager

# Khởi tạo pygame và các bước thiết lập cơ bản
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # setup màn hình
pygame.display.set_caption("WORDLE")              # tiêu đề game
timer = pygame.time.Clock()                       # setup đồng hồ
FPS = 60                                          # tốc độ khung hình

def main():

    # ---Khởi tạo các OBJECT quản lí---
    game = WordleGame()         # Quản lí logic game 
    ui = WordleUI(screen)       # Quản lí vẽ giao diện
    score_mgr = ScoreManager()  # Quản lí điểm số và đăng nhập 

    running = True

    # Biến quản lí thông báo lỗi
    warning_msg = ""
    warn_timer = 0
    cur_msg = ""

    # --- Các giá trị trạng thái của game ---
    # Game gồm nhiều trạng thái khác nhau, mỗi trạng thái đc gán 1 giá trị riêng 
    # để dễ quản lí
    # "MENU": Màn hình chọn Login/Register ban đầu
    # "AUTH": Màn hình nhập Tên/Pass
    # "SELECT_MODE": Chọn MATH hoặc WORD
    # "SELECT_DIFF": Chọn EASY hoặc HARD (đối với WORD)
    # "PLAYING": Đang chơi
    # "GAME_OVER": Kết thúc (Thắng/Thua)
    # "ASK RESUME": Hỏi người chơi muốn chơi tiếp game cũ hay không
    # "CONFRIM_EXIT": Hỏi người chơi chắc chắn muốn trở về menu chọn mode
    # "HOME_OPTION": Chọn Quit hoặc Logout
    game_state = "MENU" 
    
    # Biến kiểm soát màn hình đăng nhập
    auth_mode = "" # Sẽ là "LOGIN" hoặc "REGISTER" tùy người dùng chọn
    user_name = ""
    user_pass = ""
    active_field = 0
    # Biến này dùng để biết người chơi đang ở ô name hay ô pass
    # Nếu = 0 --> ô name
    # Nếu = 1 --> ô pass
    auth_error = ""

    # Flag dùng để kiểm soát UI vẽ các nút phụ trợ
    show_leaderboard = False
    saved_score = False # Biến dùng để kiểm tra là điểm có được lưu hay chưa, tránh tình trạng lưu nhiều lần
    show_help = False

    # Các biến lưu vị trí nút bấm (Rect) để xử lí click chuột
    # Các biến này được cập nhật liên tục thông qua ui.draw
    btn_login_rect = None
    btn_reg_rect = None
    btn_hint_rect = None
    btn_help_cir = None
    btn_rank_cir = None
    btn_undo_rect = None
    btn_settings_rect = None
    btn_home_rect = None

    inp_name_rect = None
    inp_pass_rect = None
    btn_back_auth = None

    # Biến menu mode và diff
    btn_math = None
    btn_word = None
    btn_easy = None
    btn_hard = None

    # Biến kiểm soát resume/new
    btn_ask_resume = None
    btn_ask_new = None

    # Biến kiểm soát reset
    btn_cfm_yes = None
    btn_cfm_no = None

    # Biến kiểm soát menu home
    btn_quit_rect = None
    btn_logout_rect = None

    # --- Hệ thống đồng hồ ---
    start_ticks = 0         # Thời gian bắt đầu chơi (ms)
    time_flow = 0           # Thời gian đã trôi qua (s)
    is_timer_running = False
    
    # --- VÒNG LẶP CHÍNH --- 
    while running:
        timer.tick(FPS) # giới hạn tốc độ khung hình 

        # 1. Tính toán thời gian chơi 
        if game_state == "PLAYING": # chỉ tính thời gian khi bắt đầu chơi
            if not is_timer_running:
                # Nếu mới bắt đầu chơi --> ghi nhận thời điểm bắt đầu 
                start_ticks = pygame.time.get_ticks()
                is_timer_running = True
                # Nếu không phải game cũ thì time_flow = 0
                if time_flow == 0:
                    time_flow = 0
            else:
                # Thời gian trôi qua = (Hiện tại - Bắt đầu) / 1000 
                # Hệ thống pygame sẽ ghi nhận thời điểm game bắt đầu và kết thúc
                # Nhưng ở đơn vị ms --> phải chia cho 1000
                # get_ticks() sẽ ghi nhận thời điểm theo giờ của hệ thống tại chính thời điểm chạy hàm 
                time_flow = (pygame.time.get_ticks() - start_ticks) // 1000 
        
        else:
            is_timer_running = False

        # 2. Xử lí warning (tự tắt sau vài giây)
        if warn_timer > 0:
                cur_msg = warning_msg
                ui.popup_renderer.draw_warning(screen, cur_msg)
                warn_timer -= 1
        else:
            warning_msg = ""
        
        # 3. Kiểm tra trạng thái kết thúc game
        if game_state == "PLAYING" and game.result != "":
            game_state = "GAME OVER"
            # Xóa thông tin ván chơi cũ sau khi game đó kết thúc để tránh lỗi logic
            resume.delete_last_play(user_name)

        # --- PHẦN VẼ GIAO DIỆN CHÍNH ---

        # 1. Vẽ hình nền game (bàn phím, lưới ô chữ, nút bấm)
        # Hàm này trả về vị trí các nút bấm để xử lí click chuột ở phía dưới
        btn_hint_rect, btn_help_cir, btn_rank_cir, btn_undo_rect, btn_settings_rect, btn_home_rect = ui.draw(game, warning_msg, False, time_flow)

        # 2. Vẽ các popup chồng lên, tùy vào trạng thái 
        if game_state == "ASK RESUME":
            btn_ask_resume, btn_ask_new = ui.popup_renderer.draw_resume_menu(screen, user_name)
        
        elif game_state == "MENU":
            btn_login_rect, btn_reg_rect = ui.popup_renderer.draw_start_menu(screen)

        elif game_state == "AUTH":
            if auth_mode == "LOGIN":
                title = "LOGIN FORM"
            else:
                title = "REGISTER FORM"
            inp_name_rect, inp_pass_rect, btn_back_auth = ui.popup_renderer.draw_logre_form(screen, user_name, user_pass, active_field, auth_error, title)

        elif game_state == "SELECT_MODE":
            btn_math, btn_word = ui.popup_renderer.draw_mode_selection(screen)
        
        elif game_state == "SELECT_DIFF":
            btn_easy, btn_hard = ui.popup_renderer.draw_difficulty_selection(screen)
        
        elif game_state == "GAME OVER":
            if show_leaderboard:
                ui.popup_renderer.draw_leaderboard(screen, score_mgr.get_top())
            else:
                # Vẽ kết quả thắng thua 
                ui.popup_renderer.draw_result(screen, game.result, game.ans)
                # Cập nhật điểm số 
                if game.result == "w" and not saved_score:
                    score_mgr.update_score(user_name, time_flow)
                    saved_score = True
                elif game.result == "l" and not saved_score: # Nếu ván đó thua thì không tính vào tổng thời gian chơi
                    saved_score = True
        
        elif game_state == "HOME_OPTION":
            btn_quit_rect, btn_logout_rect = ui.popup_renderer.draw_home_option(screen)

        elif game_state == "CONFIRM_EXIT":
            btn_cfm_yes, btn_cfm_no = ui.popup_renderer.draw_confirm_menu(screen)

        # 3. Vẽ các popup phụ (help, leaderboard) đè lên tất cả khi được click vào
        if show_help:
            ui.popup_renderer.draw_help(screen, game)
        
        if show_leaderboard:
            ui.popup_renderer.draw_leaderboard(screen, score_mgr.get_top())

        # Cập nhật màn hình 
        pygame.display.flip()

        #Luồng điều khiển sự kiện
        for event in pygame.event.get():
            # 1. Xử lí khi thoát game
            if event.type == pygame.QUIT:
                # Nếu đang chơi dỏ mà thoát --> lưu game
                if game_state == "PLAYING" and game.result == "":
                    game.save_state(user_name, time_flow)
                running = False

            # 2. Xử lý click chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Lưu lại vị trí của cú click
                mouse_pos = event.pos

                # Xử lí các popup đang hiện trên màn hình
                # Ấn vào vị trí bất kì để tắt popup
                if show_help:
                    show_help = False
                    continue

                if show_leaderboard:
                    show_leaderboard = False
                    continue

                # Xử lí các nút popup để hiện lên
                # Khi ấn vào thì sẽ hiện popup ngay lập tức
                if btn_rank_cir and btn_rank_cir.collidepoint(mouse_pos): # collidepoint() giúp kiểm tra cú click có nằm trong vùng kích thước của nút bấm hay không
                    show_leaderboard = True
                
                if btn_help_cir and btn_help_cir.collidepoint(mouse_pos):
                    show_help = True
                    
                # --- XỬ LÍ SỰ KIỆN THEO TỪNG TRẠNG THÁI 
                if game_state == "HOME_OPTION":
                    if btn_quit_rect and btn_quit_rect.collidepoint(mouse_pos):
                        game_state = "CONFIRM_EXIT"
                    
                    elif btn_logout_rect and btn_logout_rect.collidepoint(mouse_pos):
                        if game.result == "":
                            game.save_state(user_name, time_flow)

                        game.reset_game()
                        user_name = ""
                        user_pass = ""
                        auth_error = ""
                        game_state = "MENU"
                        
                        is_timer_running = False
                        time_flow = 0
                    # Bấm ra ngoài -> Quay lại chơi
                    else:
                        game_state = "PLAYING"
                        start_ticks = pygame.time.get_ticks() - (time_flow * 1000)
                        is_timer_running = True
                    
                elif game_state == "CONFIRM_EXIT":
                    # Nếu ấn YES -> HỦY VÁN CHƠI và về Menu
                    if btn_cfm_yes and btn_cfm_yes.collidepoint(mouse_pos):
                        # 1. Xóa file save cũ (coi như bỏ cuộc ván này)
                        resume.delete_last_play(user_name)
                        
                        # 2. Reset bàn cờ về trắng tinh
                        game.reset_game()
                        
                        # 3. Về menu chọn chế độ
                        game_state = "SELECT_MODE"
                        
                        # 4. Reset thời gian
                        is_timer_running = False
                        time_flow = 0
                    
                    # Nếu ấn NO -> Quay lại chơi tiếp 
                    if btn_cfm_no and btn_cfm_no.collidepoint(mouse_pos):
                        game_state = "PLAYING"
                        # reset start_ticks để đồng hồ chạy tiếp
                        start_ticks = pygame.time.get_ticks() - (time_flow * 1000)
                        is_timer_running = True

                elif game_state == "MENU":

                    if btn_login_rect.collidepoint(mouse_pos):
                        game_state = "AUTH"
                        auth_mode = 'LOGIN'
                        active_field = 0

                    if btn_reg_rect.collidepoint(mouse_pos):
                        game_state = "AUTH"
                        auth_mode = 'REGISTER'
                        active_field = 1

                elif game_state == "AUTH":
                    if inp_name_rect and inp_name_rect.collidepoint(mouse_pos):
                        active_field = 0
                    elif inp_pass_rect and inp_pass_rect.collidepoint(mouse_pos):
                        active_field = 1
                    elif btn_back_auth and btn_back_auth.collidepoint(mouse_pos):
                        game_state = "MENU"

                        user_name = ""
                        user_pass = ""
                        auth_error = ""
                        active_field = 0

                elif game_state == "SELECT_MODE":
                    if btn_math and btn_math.collidepoint(mouse_pos):
                        # Khởi tạo lại game ở chế độ MATH
                        game = WordleGame(mode="MATH")
                        game.reset_game()
                        # Reset đồng hồ 
                        start_ticks = pygame.time.get_ticks()
                        is_timer_running = True
                        game_state = "PLAYING"
                    
                    if btn_word and btn_word.collidepoint(mouse_pos):
                        # Nếu chọn WORD thì chuyển sang menu chọn độ khó 
                        game_state = "SELECT_DIFF"

                elif game_state == "SELECT_DIFF":
                    if btn_easy and btn_easy.collidepoint(mouse_pos):
                        game = WordleGame(mode='WORD', difficulty='EASY')
                    elif btn_hard and btn_hard.collidepoint(mouse_pos):
                        game = WordleGame(mode='WORD', difficulty='HARD')

                    # Sau khi chọn độ khó xong thì vào chơi 
                    game.reset_game()
                    start_ticks = pygame.time.get_ticks()
                    is_timer_running = True
                    game_state = "PLAYING"

                elif game_state == "PLAYING":
                    # Nút cài đặt (bật tắt bàn phím)
                    if btn_settings_rect and btn_settings_rect.collidepoint(mouse_pos):
                        settings.show_keyboard = not settings.show_keyboard
                    
                    # Nút undo
                    if btn_undo_rect and btn_undo_rect.collidepoint(mouse_pos):
                        if game.undo_guess():
                            # Phạt thời gian khi sài undo
                            # start_sticks sẽ giảm đi --> khiến time_flow tăng lên
                            start_ticks -= penalty_undo * 1000

                    # Nút hint
                    if btn_hint_rect.collidepoint(mouse_pos):
                        hint_data = game.get_hint()
                        if hint_data:
                            idx, letter = hint_data
                            start_ticks -= penalty_hint * 1000
                            warning_msg = f'HINT: Letter {idx+1} is {letter}'
                            warn_timer = 180
                        else:
                            warning_msg = "No more hints"
                            warn_timer = 60

                    # Nút home
                    if btn_home_rect and btn_home_rect.collidepoint(mouse_pos):
                        game_state = "HOME_OPTION"

                elif game_state == "ASK RESUME":
                    if btn_ask_resume and btn_ask_resume.collidepoint(mouse_pos):
                        # Nếu chọn RESUME thì load lại game cũ 
                        loaded_time = game.load_state(user_name)
                        if loaded_time:
                            time_flow = loaded_time
                            # Khi load lên cần hiển thị lại đúng thời gian đã chơi
                            # => thời gian đã chơi = cur_time - start
                            # => start = cur_time - thời gian đã chơi
                            start_ticks = pygame.time.get_ticks() - (loaded_time*1000) # nhân thêm 1000 để đổi sang giây
                            is_timer_running = True
                        game_state = "PLAYING"

                    # Nếu người chơi chọn mới thì xóa luôn ván game cũ
                    if btn_ask_new and btn_ask_new.collidepoint(mouse_pos):
                        resume.delete_last_play(user_name)
                        game_state = "SELECT_MODE"

            # 3. Xử lý bàn phím
            if event.type == pygame.KEYDOWN:
            
                # Xử lí nhập liệu login/register
                if game_state == "AUTH":
                    if event.key == pygame.K_RETURN:
                        # nếu nhập name rồi và nhấn enter thì chuyển sang ô pass 
                        if active_field == 0:
                            if len(user_name) > 0:
                                active_field = 1
                            else:
                                auth_error = "Please fill username"
                        else:
                            # Xử lí khi nhập đủ 2 ô và nhấn submit 
                            if len(user_name) > 0 and len(user_pass) > 0:
                                if auth_mode == "REGISTER": 
                                    success, msg = score_mgr.register(user_name, user_pass)
                                else:
                                    success, msg = score_mgr.login(user_name, user_pass)
                                
                                # Khi login/register thành công
                                # Nếu register --> hiện menu chọn mode
                                # Nếu login --> kiểm tra có game cũ không ----> nếu có: hỏi có muốn chơi lại hay không
                                #                                         |
                                #                                         ----> nếu ko: hiện menu chọn mode
                                if success:
                                    if auth_mode == "REGISTER":
                                        game_state = "SELECT_MODE"
                                    elif auth_mode == "LOGIN":
                                        if game.check_has_save(user_name):
                                            game_state = "ASK RESUME" 
                                        else:
                                            game_state = "SELECT_MODE"
                                else:
                                    auth_error = msg # Hiện lỗi (sai pass, trùng tên)
                            else:
                                auth_error = "PLEASE FILL ALL FIELDS"

                    elif event.key == pygame.K_TAB: # có thể dùng phím tab để chuyển ô
                        active_field = 1 - active_field 
                            
                    # Xử lí khi ấn nút xóa
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == 0:
                            user_name = user_name[:-1]
                        else:
                            user_pass = user_pass[:-1]
                        auth_error = "" # xóa lỗi khi gõ lại 

                    else:
                        char = event.unicode # Lấy kí tự vừa nhấn
                        
                        # Nhập TÊN (Chỉ chữ, số, gạch dưới)
                        if active_field == 0:
                            # Chỉ cho phép chữ, số và dấu "_" 
                            if (char.isalnum() or char == "_") and len(user_name) < 20:
                                user_name += char

                        # Nhập Pass (ho phép @, #, !,...)
                        elif active_field == 1:
                            # isprintable() chấp nhận mọi ký tự in được ra màn hình
                            if char.isprintable() and len(user_pass) < 20:
                                user_pass += char

                # --- XỬ LÍ KHI GAME OVER ---
                elif game_state == "GAME OVER":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if not show_leaderboard:
                            show_leaderboard = True     # Hiện bảng xếp hạng trước
                        else:
                            # Chơi lại ván mới 
                            game.reset_game()
                            game_state = "PLAYING"
                            show_leaderboard = False
                            saved_score = False

                            # Reset đồng hồ 
                            start_ticks = pygame.time.get_ticks()
                            time_flow = 0
                            is_timer_running = True

                    # Quay lại menu chọn mode khi nhấn ESC
                    elif event.key == pygame.K_ESCAPE:
                        if game_state == "PLAYING" or game_state == "GAME OVER":
                        # Nếu đang chơi dở thì lưu lại
                            if game_state == "PLAYING" and game.result == "":
                                game.save_state(user_name, time_flow)
                            
                            game.reset_game()
                            game_state = "SELECT_MODE" # Về SELECT_MODE 
                            
                            # Reset UI phụ
                            show_leaderboard = False
                            saved_score = False
                            
                            # Reset thời gian
                            is_timer_running = False
                            time_flow = 0
                            # Không reset user_name/user_pass để giữ đăng nhập
                
                # --- XỬ LÍ KHI ĐANG CHƠI --- 
                elif game_state == "PLAYING":
                    # Xóa thông báo lỗi cũ khi ấn phím bất kì 
                    if warn_timer > 0:
                        warn_timer = 0
                        warning_msg = ""
                    
                    # Nếu game chưa kết thúc
                    if event.key == pygame.K_BACKSPACE:
                        game.remove_letter()

                    elif event.key == pygame.K_RETURN:
                        status = game.submit_guess()

                        if status == "invalid_word":
                            if game.mode == 'WORD':
                                warning_msg = "Word not found!"
                            else:
                                warning_msg = "Invalid expression!"
                            warn_timer = 60
                        else:
                            # Mỗi lần đoán xong thì AUTO SAVE
                            game.save_state(user_name, time_flow)

                    elif event.key == pygame.K_LEFT: # phím tắt undo 
                        if game.undo_guess():
                            start_ticks -= penalty_undo * 1000
                    else: 
                        # Nhập kí tự 
                        if game.mode == 'WORD':
                            if event.unicode.isalpha():
                                game.add_letter(event.unicode.upper())
                        else:
                            if event.unicode in "0123456789+-*/=":
                                game.add_letter(event.unicode)

    pygame.quit()

if __name__ == "__main__":
    main()