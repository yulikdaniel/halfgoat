import pygame
from pygame.locals import *
import random
from time import time
from config import alph, cons, minv, minc
import checker.new_check as checker

checker.build()

iconImg = pygame.image.load("pics/Icon.png")

BW, BH = 50, 50
WIDTH, HEIGHT = 20, 20
A, B = WIDTH * BW, HEIGHT * BH
MENUWIDTH = 800

pygame.init()
pygame.display.set_icon(iconImg)
pygame.display.set_caption("Semigoat")
font = pygame.font.SysFont("comicsansms", 40)
display = pygame.display.set_mode((A + MENUWIDTH, B))
clock = pygame.time.Clock()

FPS = 60

LIGHT_YELLOW = (255, 255, 153)
LIGHT_RED = (255, 153, 153)
LIGHT_GREEN = (150, 250, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)

HIGHLIGHT_COLOUR = LIGHT_YELLOW
HIGHLIGHT_CORRECT = LIGHT_GREEN
HIGHLIGHT_WRONG = LIGHT_RED

COLOURS = [GREEN, RED, BLUE, ORANGE]
t1 = 0


def draw_square(col, x, y, width=0):
    pygame.draw.rect(display, col, (x * BW + 3, y * BH + 3, BW - 6, BH - 6), width=width)


def draw_blank():
    display.fill(WHITE)
    for x in range(0, A + 1, BW):
        pygame.draw.line(display, GREY, (x, 0), (x, A))
    for y in range(0, B + 1, BH):
        pygame.draw.line(display, GREY, (0, y), (B, y))


def tech_pygame():
    global t1
    pygame.display.update()
    clock.tick(FPS)
    # print(round(1/(time() - t1)))
    t1 = time()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONUP:
            cursor.process_up()
        if event.type == MOUSEBUTTONDOWN:
            cursor.process_down()
            menu.on_click()


def inField(x, y):
    return x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT


def generate_letters(seed=None):
    if seed is not None:
        random.seed(seed)
    letters = []
    sm = sum([x[1] for x in alph])
    while not letters:
        numc = 0
        numv = 0
        for x in range(20):
            t = random.random() * sm
            for let, pr in alph:
                if t < pr:
                    letters.append(let)
                    break
                t -= pr
            if cons[letters[-1]] == 0:
                numv += 1
            if cons[letters[-1]] == 1:
                numc += 1
        if numc < minc or numv < minv:
            letters = []
    return letters


class Field:
    def __init__(self, letters):
        self.field = [['' for x in range(WIDTH)] for y in range(HEIGHT)]
        self.spellcheck = True
        self.scorecount = True
        self.highlight = None
        for i in range(len(letters)):
            self.field[0][i] = letters[i]

    def draw(self):
        draw_blank()
        self.highlight = [[set() for x in range(WIDTH)] for y in range(HEIGHT)]
        if self.spellcheck:
            self.highlight_correct()
        self.draw_highlight()
        cursor.highlight()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.field[y][x]:
                    display.blit(font.render(self.field[y][x], True, BLACK), (x * BW + 10, y * BW - 8))
        if self.scorecount:
            display.blit(font.render("SCORE: ", True, BLACK), ((WIDTH + 3) * BW, BH))
            display.blit(font.render(str(count_score(self)), True, BLACK), ((WIDTH + 3) * BW + font.size("SCORE: ")[0], BH))

    def highlight_correct(self):
        for x in range(WIDTH):
            cur = 0
            for y in range(HEIGHT):
                if self.field[y][x]:
                    cur += 1
                else:
                    if cur > 1:
                        self.highlight_word(x, y - cur, cur, True)
                    cur = 0
            if cur > 1:
                self.highlight_word(x, y - cur + 1, cur, True)

        for y in range(HEIGHT):
            cur = 0
            for x in range(WIDTH):
                if self.field[y][x]:
                    cur += 1
                else:
                    if cur > 1:
                        self.highlight_word(x - cur, y, cur, False)
                    cur = 0
            if cur > 1:
                self.highlight_word(x - cur + 1, y, cur, False)

    def highlight_word(self, sx, sy, cur, vertical):
        word = ""
        for x in range(sx, sx + 1 + (not vertical) * (cur - 1)):
            for y in range(sy, sy + 1 + vertical * (cur - 1)):
                word += self.field[y][x]

        if checker.check_word(word):
            col = HIGHLIGHT_CORRECT
        else:
            col = HIGHLIGHT_WRONG

        for x in range(sx, sx + 1 + (not vertical) * (cur - 1)):
            for y in range(sy, sy + 1 + vertical * (cur - 1)):
                self.highlight[y][x].add(col)

    def draw_highlight(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if len(self.highlight[y][x]) == 0:
                    continue
                res = [0, 0, 0]
                for col in self.highlight[y][x]:
                    for i in range(3):
                        res[i] += col[i]
                for i in range(3):
                    res[i] /= len(self.highlight[y][x])
                draw_square(tuple(res), x, y)


def count_score(field):
    print('\n\n\n\n')
    score = 0
    for x in range(WIDTH):
        curl = 0
        for y in range(HEIGHT):
            if field.field[y][x]:
                curl += 1
                score += max(0, (curl - 5) // 2)
            else:
                curl = 0
    for y in range(HEIGHT):
        curl = 0
        for x in range(WIDTH):
            if field.field[y][x]:
                curl += 1
                score += max(0, (curl - 5) // 2)
            else:
                curl = 0

    used = [[False for x in range(WIDTH)] for y in range(HEIGHT)]


    def dfs(x, y, used, s):
        used[y][x] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT and field.field[y + dy][x + dx]:
                if used[y + dy][x + dx]:
                    pass # TODO something about the circles
                else:
                    s.add((abs(dx), abs(dy)))
                    dfs(x + dx, y + dy, used, s)


    numc = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if field.field[y][x] and not used[y][x]:
                cur = None
                s = set()
                dfs(x, y, used, s)
                numc += 1

    if numc == 1:
        score += 2

    return score


def toggle_spellcheck(nstate):
    gameField.spellcheck = not gameField.spellcheck


def toggle_scorecount(nstate):
    gameField.scorecount = not gameField.scorecount


class Tick:
    def __init__(self, text, effect, y0, state=False):
        self.text = text
        self.effect = effect
        self.state = state
        self.highlight = False
        self.y = y0 + 5
        self.x = WIDTH + 3

    def draw(self):
        draw_square(GREY, self.x, self.y, width=3)
        if self.highlight:
            draw_square(HIGHLIGHT_COLOUR, self.x, self.y)
        if self.state:
            pygame.draw.line(display, BLACK, (self.x * BW + 10, self.y * BH + 15), (self.x * BW + BW // 2, (self.y + 1) * BH - 10), width=4)
            pygame.draw.line(display, BLACK, (self.x * BW + BW // 2, (self.y + 1) * BH - 10), ((self.x + 1) * BW - 10, self.y * BH + 7), width=4)
        display.blit(font.render(self.text, True, BLACK), (A + 4 * BW + 10, BH * self.y - 5))

    def check_highlight(self, pos_x, pos_y):
        if self.x * BW <= pos_x <= (self.x + 1) * BW and self.y * BH <= pos_y <= (self.y + 1) * BH:
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        if self.highlight:
            self.state = not self.state
            self.effect(self.state)


class Menu:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self):
        self.highlight()
        for y in range(len(self.buttons)):
            self.buttons[y].draw()

    def highlight(self):
        x, y = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_highlight(x, y)

    def on_click(self):
        for button in self.buttons:
            button.on_click()


class Cursor:
    def __init__(self):
        self.carry = ''
        self.cellx = -1
        self.celly = -1
        self.x = -1
        self.y = -1
        self.left_since_down = False

    def process_up(self):
        if self.carry and (self.left_since_down != (self.carry == '')):
            self.carry, gameField.field[self.celly][self.cellx] = gameField.field[self.celly][self.cellx], self.carry

    def process_down(self):
        if not self.carry and gameField.field[self.celly][self.cellx]:
            self.carry = gameField.field[self.celly][self.cellx]
            gameField.field[self.celly][self.cellx] = ''
            self.left_since_down = False

    def update_coords(self):
        self.x, self.y = pygame.mouse.get_pos()
        ox, oy = self.cellx, self.celly
        self.cellx, self.celly = min(WIDTH - 1, self.x // BW), min(HEIGHT - 1, self.y // BH)
        if (ox, oy) != (self.cellx, self.celly):
            self.left_since_down = True

    def highlight(self):
        draw_square(HIGHLIGHT_COLOUR, self.cellx, self.celly)

    def draw_carry(self):
        if self.carry:
            display.blit(font.render(self.carry, True, BLACK), (self.cellx * BW + 10, self.celly * BW - 8))


gameField = Field(generate_letters(1543))
cursor = Cursor()
menu = Menu([
                Tick("Spellcheck", toggle_spellcheck, 0, True),
                Tick("Score Count", toggle_scorecount, 1, True)
            ])

curx, cury = 0, 0

while True:
    cursor.update_coords()
    gameField.draw()
    cursor.draw_carry()
    menu.draw()
    tech_pygame()
