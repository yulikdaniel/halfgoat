import random

import pygame

import checker.new_check as checker
from config import CONSTANTS, config, display


def draw_square_pos(col, x, y, xsz=CONSTANTS.BW, ysz=CONSTANTS.BH, width=0):
    pygame.draw.rect(display, col, (x, y, xsz, ysz), width=width)


def draw_square(col, x, y, width=0):
    pygame.draw.rect(
        display, col, (x * CONSTANTS.BW + 3, y * CONSTANTS.BH + 3, CONSTANTS.BW - 6, CONSTANTS.BH - 6), width=width
    )


def draw_blank():
    display.fill(config.colours.colours_list["white"])
    for x in range(0, CONSTANTS.A + 1, CONSTANTS.BW):
        pygame.draw.line(display, config.colours.colours_list["grey"], (x, 0), (x, CONSTANTS.B))
    for y in range(0, CONSTANTS.B + 1, CONSTANTS.BH):
        pygame.draw.line(display, config.colours.colours_list["grey"], (0, y), (CONSTANTS.A, y))


def inField(x, y):
    return x >= 0 and y >= 0 and x < CONSTANTS.WIDTH and y < CONSTANTS.HEIGHT


def generate_letters(seed=None):
    if seed is not None:
        random.seed(seed)
    while True:
        letters = random.choices(
            population=list(config.letters.probability.keys()),
            weights=list(config.letters.probability.values()),
            k=20,
        )
        if sum(1 for let in letters if let in config.letters.vowels) < config.letters.min_vowel_amt:
            continue
        if sum(1 for let in letters if let in config.letters.consonants) < config.letters.min_consonant_amt:
            continue
        return letters


class Field:
    def __init__(self, letters):
        self.field = [['' for x in range(CONSTANTS.WIDTH)] for y in range(CONSTANTS.HEIGHT)]
        self.spellcheck = True
        self.scorecount = True
        self.highlight = None
        for i in range(len(letters)):
            self.field[0][i] = letters[i]

    def draw(self):
        draw_blank()
        self.highlight = [[set() for x in range(CONSTANTS.WIDTH)] for y in range(CONSTANTS.HEIGHT)]
        if self.spellcheck:
            self.highlight_correct()
        self.draw_highlight()
        self.cursor.highlight()
        for x in range(CONSTANTS.WIDTH):
            for y in range(CONSTANTS.HEIGHT):
                if self.field[y][x]:
                    display.blit(
                        CONSTANTS.font.render(self.field[y][x], True, config.colours.colours_list["black"]),
                        ((x + 0.2) * CONSTANTS.BW, (y + 0.1) * CONSTANTS.BH),
                    )
        if self.scorecount:
            display.blit(
                CONSTANTS.font.render("SCORE: ", True, config.colours.colours_list["black"]),
                ((CONSTANTS.WIDTH + 3) * CONSTANTS.BW, CONSTANTS.BH),
            )
            display.blit(
                CONSTANTS.font.render(str(count_score(self)), True, config.colours.colours_list["black"]),
                ((CONSTANTS.WIDTH + 3) * CONSTANTS.BW + CONSTANTS.font.size("SCORE: ")[0], CONSTANTS.BH),
            )

    def highlight_correct(self):
        for x in range(CONSTANTS.WIDTH):
            cur = 0
            for y in range(CONSTANTS.HEIGHT):
                if self.field[y][x]:
                    cur += 1
                else:
                    if cur > 1:
                        self.highlight_word(x, y - cur, cur, True)
                    cur = 0
            if cur > 1:
                self.highlight_word(x, y - cur + 1, cur, True)

        for y in range(CONSTANTS.HEIGHT):
            cur = 0
            for x in range(CONSTANTS.WIDTH):
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
            col = config.colours.highlight_correct
        else:
            col = config.colours.highlight_wrong

        for x in range(sx, sx + 1 + (not vertical) * (cur - 1)):
            for y in range(sy, sy + 1 + vertical * (cur - 1)):
                self.highlight[y][x].add(col)

    def draw_highlight(self):
        for x in range(CONSTANTS.WIDTH):
            for y in range(CONSTANTS.HEIGHT):
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
    score = 0
    for x in range(CONSTANTS.WIDTH):
        curl = 0
        for y in range(CONSTANTS.HEIGHT):
            if field.field[y][x]:
                curl += 1
                score += max(0, (curl - 4) // 2)
            else:
                curl = 0
    for y in range(CONSTANTS.HEIGHT):
        curl = 0
        for x in range(CONSTANTS.WIDTH):
            if field.field[y][x]:
                curl += 1
                score += max(0, (curl - 4) // 2)
            else:
                curl = 0

    used = [[False for x in range(CONSTANTS.WIDTH)] for y in range(CONSTANTS.HEIGHT)]

    def dfs(x, y, used, s, xf, yf):
        ring_score = 0
        used[y][x] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x + dx < CONSTANTS.WIDTH and 0 <= y + dy < CONSTANTS.HEIGHT and field.field[y + dy][x + dx]:
                if used[y + dy][x + dx]:
                    if (xf, yf) != (x + dx, y + dy):
                        ring_score += 1
                else:
                    s.add((abs(dx), abs(dy)))
                    ring_score += dfs(x + dx, y + dy, used, s, x, y)
        return ring_score

    numc = 0
    for y in range(CONSTANTS.HEIGHT):
        for x in range(CONSTANTS.WIDTH):
            if field.field[y][x] and not used[y][x]:
                s = set()
                ring = dfs(x, y, used, s, -1, -1)
                score += ring // 2
                if len(s) <= 1:
                    score -= 1
                numc += 1

    if numc == 1:
        score += 2

    return score


def toggle_spellcheck(field, instance):
    instance.state = not instance.state
    field.spellcheck = not field.spellcheck


def toggle_scorecount(field, instance):
    instance.state = not instance.state
    field.scorecount = not field.scorecount


NUM_FIELDS = 3
fields = [0 for x in range(NUM_FIELDS)]
carry = ['' for x in range(NUM_FIELDS)]
cur_num = 0


def current_checkpoint():
    return cur_num


def switch_checkpoint(field, number, instance):
    global fields, cur_num
    fields[cur_num] = field.field
    carry[cur_num] = field.cursor.carry
    if fields[number] == 0:
        fields[number] = [x.copy() for x in fields[cur_num]]
        carry[number] = carry[cur_num]
    cur_num = number
    field.field = fields[cur_num]
    field.cursor.carry = carry[cur_num]
