import os
from random import random, shuffle
from logics import *
import pygame
import sys
from database import *
import json
USERNAME = None
def init_const():
    global score, mas
    mas = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]
    score = 0
    empty = get_empty_list(mas)
    shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1,y1 = get_index_from_number(random_num1)
    insert_2_or_4(mas, x1, y1)
    x2,y2 = get_index_from_number(random_num2)
    insert_2_or_4(mas, x2, y2)
mas = None
score = None
path = os.getcwd()
if 'data.txt' in os.listdir(path):
    with open('data.txt','r') as file:
        data = json.load(file)
        mas = data['mas']
        score = data['score']
        USERNAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
else:
    init_const()

def draw_intro():
    img2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('comicsansms', 60)
    text_welcome = font.render('Welcome!', True, WHITE)
    name = 'Введите имя'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and len(name) > 2:
                    global USERNAME
                    USERNAME = name
                    is_find_name = True
                    break
        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        screen.blit(text_welcome, (230, 80))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)

def draw_game_over():
    global GAMERS_DB
    global USERNAME, mas, score
    img2048 = pygame.image.load('2048_logo.png')
    font= pygame.font.SysFont('comicsansms', 50)
    text_game_over = font.render('Game over!', True, WHITE)
    text_score = font.render(f'Вы набрали {score} очков', True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'Рекорд побит'
    else:
        text = f'Рекорд - {best_score}'
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    GAMERS_DB = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_decision = True
                    init_const()
        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 80))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        pygame.display.update()
    screen.fill(BLACK)
GAMERS_DB = get_best()

def draw_top_gamers():
    font_top = pygame.font.SysFont('comicsansms', 26)
    font_gamer = pygame.font.SysFont('comicsansms', 22)
    text_head = font_top.render('Best tries:', True, COLOR_TEXT)
    screen.blit(text_head, (250, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index+1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (250, 30 + 25 * index))
        print(index, name, score)

def draw_interface(score, delta = 0):
        pygame.draw.rect(screen, WHITE, TITLE_REC)
        font = pygame.font.SysFont('comicsansms', 65)
        font_score = pygame.font.SysFont('comicsansms', 42)
        font_delta = pygame.font.SysFont('comicsansms', 28)
        text_score = font_score.render('Score:', True, COLOR_TEXT)
        text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
        screen.blit(text_score, (20,35))
        screen.blit(text_score_value, (175, 35))
        if delta:
            text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
            screen.blit(text_delta, (170,65))
        draw_top_gamers()
        pretty_print(mas)
        for row in range(BLOCKS):
            for column in range(BLOCKS):
                value = mas[row][column]
                text = font.render(f'{value}', True, BLACK)
                w = column * SIZE_BLOCK + (column+1) * MARGIN
                h = row * SIZE_BLOCK + (row+1) * MARGIN + SIZE_BLOCK
                pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
                if value != 0:
                    font_w, font_h = text.get_size()
                    text_x = w + (SIZE_BLOCK - font_w) / 2
                    text_y = h + (SIZE_BLOCK - font_h) / 2
                    screen.blit(text, (text_x, text_y))
COLOR_TEXT = (255, 127, 0)
COLORS = {
    0 : (130, 130, 130),
    2 : (255, 255, 255),
    4 : (255, 255, 128),
    8 : (255, 255, 0),
    16 : (255, 128, 0),
    32 : (255, 0, 0),
    64 : (128, 0, 0),
    128 : (112, 0, 0),
    256 : (96, 0, 0),
    512 : (80, 0, 0),
    1024 : (64, 0, 0),
    2048 : (32, 0, 0)
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


#for gamer in get_best():
#    print(gamer)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
draw_interface(score)
pygame.display.update()
def save_game():
    data = {
        'user' : USERNAME,
        'score' : score,
        'mas' : mas
    }
    with open('data.txt','w') as outfile:
        json.dump(data, outfile)

def game_loop():
    global score, mas
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                is_mas_moved = False
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_moved = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_moved = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_moved = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta,is_mas_moved = move_down(mas)
                score += delta
                if is_zero_in_mas(mas) and is_mas_moved:
                    empty = get_empty_list(mas)
                    shuffle(empty)
                    random_num = empty.pop()
                    x,y = get_index_from_number(random_num)
                    insert_2_or_4(mas, x, y)
                    print(f'Мы заполнили элемент под номером {random_num}')
                draw_interface(score, delta)
                pygame.display.update()

        print(USERNAME)

while True:
    if USERNAME is None:
       draw_intro()
    game_loop()
    draw_game_over()