import pygame
import pygame_menu
import sys
from random import randint
pygame.init()
bg_image = pygame.image.load('logo.png')
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (254, 0, 0)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_MARGIN = 70
size = (SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * (COUNT_BLOCKS + 2) + MARGIN * COUNT_BLOCKS + HEADER_MARGIN)
courier = pygame.font.SysFont('courier', 36)


screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS


def draw_block(color, row, column):
        pygame.draw.rect(screen, color, (SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                        SIZE_BLOCK + HEADER_MARGIN + row * SIZE_BLOCK + MARGIN * (row + 1),
                                        SIZE_BLOCK, SIZE_BLOCK))

def get_random_empty_block():
    x = randint(0, COUNT_BLOCKS - 1)
    y = randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        x = randint(0, COUNT_BLOCKS - 1)
        y = randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
    return empty_block

snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
apple = get_random_empty_block()
d_row = buf_row = 0
d_col = buf_col = 1
pygame.init()
surface = pygame.display.set_mode((460, 530))

def start_the_game():
    total = 0
    speed = 1
    def get_random_empty_block():
        x = randint(0, COUNT_BLOCKS - 1)
        y = randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            x = randint(0, COUNT_BLOCKS - 1)
            y = randint(0, COUNT_BLOCKS - 1)
            empty_block = SnakeBlock(x, y)
        return empty_block
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, (0, 0, size[0], HEADER_MARGIN))
        text_total = courier.render(f'Total: {total}', 0, WHITE)
        text_speed = courier.render(f'Speed: {speed}', 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 210, SIZE_BLOCK))
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (column + row) % 2:
                    color = WHITE
                else:
                    color = BLUE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            break
        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)
        pygame.display.update()
        if apple == head:
            total += 1
            speed = 1 + total // 5
            snake_blocks.append(apple)
            apple = get_random_empty_block()
        d_row = buf_row
        d_col = buf_col

        new_head = SnakeBlock(head.x + d_row,head.y + d_col)

        if new_head in snake_blocks:
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(2 + speed)


menu = pygame_menu.Menu('', 220, 300,
                       theme=pygame_menu.themes.THEME_GREEN)

menu.add.text_input('Имя: ', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)
while True:
    screen.fill(WHITE)
    screen.blit(pygame.transform.scale(bg_image, (460, 530)), (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
            sys.exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()