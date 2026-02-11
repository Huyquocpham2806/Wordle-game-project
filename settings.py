import pygame

# Định nghĩa màu sắc
background = (18, 18, 19)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (100, 100, 100)
green = (106, 170, 100)
dark_green = (34, 139, 34)
yellow = (201, 180, 88)
red = (255, 0, 0)
outline = (129, 131, 132)
pink = (255, 105, 180)
dark_black = (18, 18, 19)
beige = (240, 235, 215)
light_gray = (211, 211, 211)
orange = (255, 140, 0)

#giao diện game 
WIDTH = 600
HEIGHT = 800
box_size = 70
gap = 10
margin_top = 100
margin_left = (WIDTH - (5 * box_size + 4 * gap)) // 2

#KEYBOARD SETUP
key_width = 40
key_height = 55
key_gap = 6
keyboard_y_start = 600
show_keyboard = True

# mức phạt
penalty_hint = 15
penalty_undo = 30

qwerty = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

num_layout = [
    "1234567890",
    "+-*/="
]
