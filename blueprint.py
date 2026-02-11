import pygame
import random

pygame.init()

#screen setup
background = (18, 18, 19)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (100, 100, 100)
green = (106, 170, 100)
yellow = (201, 180, 88)
red = (255, 0, 0)
outline = (129, 131, 132)
pink = (255, 182, 193)


WIDTH = 600
HEIGHT = 800
box_size = 70
gap = 10
margin_top = 100
margin_left = (WIDTH - (5 * box_size + 4 * gap)) // 2

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("WORDLE")    

fps = 60
timer = pygame.time.Clock()
FONT = pygame.font.Font('freesansbold.ttf', 40)
RESULT_FONT = pygame.font.Font('freesansbold.ttf', 20)
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 50)
KEY_FONT = pygame.font.Font('freesansbold.ttf', 30)



#RESULT SETUP
rs_width = 300
rs_height = 100
rs_start_x = 150
rs_start_y = 300

#WARNING SETUP
warn_width = 250
warn_height = 100
warn_start_x = 175
warn_start_y = 300

#KEYBOARD SETUP
key_width = 40
key_height = 55
key_gap = 6
keyboard_y_start = 600

qwerty = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

key_colors = {} 
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    key_colors[char] = outline



def load_data():
    with open('English (EZ dataset).txt', 'r') as inp:
        data = [word.strip().upper() for word in inp.readlines()]

    with open('English (Hard dataset).txt', 'r') as f:
        valid_guess = [word.strip().upper() for word in f.readlines()]
    
    avai = set(data + valid_guess)
    return data, avai

def draw_warning(warning_msg):
    # Dùng font nhỏ hơn chút cho thông báo lỗi

    rect = pygame.Rect(warn_start_x, warn_start_y, warn_width, warn_height)
    pygame.draw.rect(screen, white, rect, border_radius=4)

    small_font = pygame.font.Font('freesansbold.ttf', 25)
    warn_surf = small_font.render(warning_msg, True, red)
    warn_rect = warn_surf.get_rect(center=rect.center) # Hiện ở trên đầu bảng
    screen.blit(warn_surf, warn_rect)

def check_guess(guess, ans):
    result_colors = [gray]*5
    ans_letter = list(ans)

    for i in range(5):
        if guess[i] == ans[i]:
            result_colors[i] = green
            ans_letter[i] = None
            key_colors[guess[i]] = green
        
    for i in range(5):
        if result_colors[i] != green:
            if guess[i] in ans_letter:
                result_colors[i] = yellow
                ans_letter.remove(guess[i])
                if key_colors[guess[i]] != green:
                    key_colors[guess[i]] = yellow
            elif key_colors[guess[i]] != green and key_colors[guess[i]] != yellow:
                key_colors[guess[i]] = gray

    return result_colors

def draw_keyboard():
    for i in range(len(qwerty)):

        row_chars = qwerty[i]
        row_width = len(row_chars)*(key_width + key_gap) - key_gap
        st_x = (WIDTH - row_width)//2
        y = keyboard_y_start + i*(key_height + key_gap)

        for j in range(len(row_chars)):

            char = row_chars[j]
            x = st_x + j*(key_width + key_gap)
            rect = pygame.Rect(x, y, key_width, key_height)

            bg_color = key_colors[char]
            
            if bg_color == outline:
                pygame.draw.rect(screen, bg_color, rect, 4, border_radius = 4)
            else:
                pygame.draw.rect(screen, bg_color, rect, border_radius = 4)

            text_surf = KEY_FONT.render(char, True, white)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

def draw_title():

    title_surf = TITLE_FONT.render("WORDLE", True, white)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    screen.blit(title_surf, title_rect)

    #pygame.draw.line(surface, color, start_pos, end_pos, width)
    pygame.draw.line(screen, gray, (0, 85), (WIDTH, 85), 1)

def draw_result(result, ans):

    msg = "Press SPACE to play again"
    sub_msg = f"The answer is: {ans}"

    msg1 = ""
    if result == "w":
        msg1 = f"YOU WIN"
        color = green
    
    elif result == "l":
        msg1 = f"YOU LOSE"
        color = red
        

    rect = pygame.Rect(rs_start_x, rs_start_y, rs_width, rs_height)
    pygame.draw.rect(screen, color, rect, border_radius=10)

    if result == 'l':
        text_surface2 = RESULT_FONT.render(sub_msg, True, white)
        text_rect2 = text_surface2.get_rect(center=rect.center)
        screen.blit(text_surface2, text_rect2)

        text_surface1 = RESULT_FONT.render(msg1, True, white)
        text_rect1 = text_surface1.get_rect(center=(rect.centerx, rect.centery - 30))
        screen.blit(text_surface1, text_rect1)

        text_surface = RESULT_FONT.render(msg, True, white)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + 30))
        screen.blit(text_surface, text_rect)

    else:
        text_surface1 = RESULT_FONT.render(msg1, True, white)
        text_rect1 = text_surface1.get_rect(center=(rect.centerx, rect.centery - 20))
        screen.blit(text_surface1, text_rect1)

        text_surface = RESULT_FONT.render(msg, True, white)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + 20))
        screen.blit(text_surface, text_rect)



def draw_board(current_word, word_list, answer):

    draw_title()
    draw_keyboard()

    for row in range(6):
        row_color = []
        if row < len(word_list):
            row_color = check_guess(word_list[row], answer)
        for col in range(5):
            # Rect(x, y, width, height)
            #pygame.draw.rect(screen, color, rect, width, border radius)
            x = margin_left + col*(box_size + gap)
            y = margin_top + row*(box_size + gap)
            rect = pygame.Rect(x, y, box_size, box_size)
            pygame.draw.rect(screen, white, rect, 3, 10)

            if row < len(word_list): # vẽ màu của hàng cũ
                cell_color = row_color[col]
                pygame.draw.rect(screen, cell_color, rect, border_radius = 10)
            else: # vẽ màu của hàng hiện tại
                color = outline
                if row == len(word_list) and col < len(current_word):
                    color = pink # Viền sáng lên chút khi đang gõ 
                pygame.draw.rect(screen, color, rect, 2, border_radius=10)

            char = None

            if row < len(word_list): # vẽ các từ trong quá khứ
                char = word_list[row][col] 
            elif row == len(word_list): # vẽ các từ ở hiện tại
                if col < len(current_word):
                    char = current_word[col]

            if char:
                text_surface = FONT.render(char, True, white)
                text_rect = text_surface.get_rect(center=rect.center)
                #screen.blit(source(từ đâu), dest(vào đâu)): dán hình ảnh từ source vào dest
                screen.blit(text_surface, text_rect)

def main():
    current_guess = ""
    guess = []
    running = True
    result = ""
    warning_msg = ""
    warn_time = 0
    solutions, available = load_data()
    ans = random.choice(solutions).upper()

    #tạo màn mờ
    dim_surface = pygame.Surface((WIDTH, HEIGHT))   
    dim_surface.fill(black)
    dim_surface.set_alpha(180)


    while running:
        timer.tick(fps)
        screen.fill(background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if warn_time > 0 and event.key == pygame.K_BACKSPACE:
                    warn_time = 0
                if result != "" and event.key == pygame.K_SPACE:
                    guess = []
                    current_guess = ""
                    ans = random.choice(solutions).upper()
                    result = ""
                    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        key_colors[char] = outline

                elif result == "":

                    if event.key == pygame.K_BACKSPACE:
                        if len(current_guess) > 0:
                            current_guess = current_guess[:-1]

                    elif event.key == pygame.K_RETURN:
                        if len(current_guess) == 5 and len(guess) <= 6:
                            if current_guess in available:
                                guess.append(current_guess)
                                if current_guess == ans:
                                    result = "w"
                                elif len(guess) == 6:
                                    result = "l"
                                current_guess = ""
                            else:
                                warning_msg = "Word not found!"
                                warn_time = 180
                        
                    else:
                        key_word = event.unicode.upper()
                        if key_word.isalpha() and len(current_guess) < 5:
                            current_guess += key_word


        draw_board(current_guess, guess, ans)

        if warn_time > 0:
            screen.blit(dim_surface, (0, 0))
            draw_warning(warning_msg)
            warn_time -= 1

        if result != "":
           screen.blit(dim_surface, (0, 0))
           draw_result(result, ans)


        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()