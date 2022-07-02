import pygame

from config import *
from field import *


class Tick:
    def __init__(self, text, effect, x0=0, y0=0, state=False):
        self.text = text
        self.effect = effect
        self.state = state
        self.highlight = False
        self.y = y0
        self.x = x0

    def draw(self, offsetx, offsety):
        offsetx += self.x
        offsety += self.y
        draw_square_pos(GREY, offsetx, offsety - 10, width=3)
        if self.highlight:
            draw_square_pos(HIGHLIGHT_COLOUR, offsetx, offsety - 10)
        if self.state:
            pygame.draw.line(
                display, BLACK, (offsetx + 10, offsety + 5), (offsetx + BW // 2, offsety + BH - 20), width=4
            )
            pygame.draw.line(
                display, BLACK, (offsetx + BW // 2, offsety + BH - 20), (offsetx + BW - 10, offsety - 3), width=4
            )
        display.blit(font.render(self.text, True, BLACK), (offsetx + BW + 10, offsety))

    def check_highlight(self, pos_x, pos_y):
        if self.x <= pos_x <= self.x + BW and self.y <= pos_y + 10 <= self.y + BH:
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        if self.highlight:
            self.effect(self)


class Button:
    def __init__(self, text, effect, x0=0, y0=0):
        self.text = text
        self.effect = effect
        self.highlight = False
        self.y = y0
        self.x = x0
        self.texts = [font.render(self.text, True, BLACK), font.render(self.text, True, TEXT_HIGHLIGHT_COLOUR)]

    def draw(self, offsetx, offsety):
        display.blit(self.texts[self.highlight], (self.x + offsetx, self.y + offsety))

    def check_highlight(self, pos_x, pos_y):
        if (
            self.x <= pos_x <= self.x + self.texts[self.highlight].get_width()
            and self.y <= pos_y <= self.y + self.texts[self.highlight].get_height()
        ):
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        if self.highlight:
            self.effect(self)


class Info:
    def __init__(self, getText, x0=0, y0=0):
        self.highlight = False
        self.y = y0
        self.x = x0
        self.getText = lambda: font.render(getText if isinstance(getText, str) else getText(), True, BLACK)

    def draw(self, offsetx, offsety):
        display.blit(self.getText(), (self.x + offsetx, self.y + offsety))

    def check_highlight(self, pos_x, pos_y):
        if (
            self.x <= pos_x <= self.x + self.getText().get_width()
            and self.y <= pos_y <= self.y + self.getText().get_height()
        ):
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        return


class Menu:
    def __init__(self, buttons, offsetx, offsety):
        self.buttons = buttons
        self.offsetx, self.offsety = offsetx, offsety

    def draw(self):
        self.highlight()
        for y in range(len(self.buttons)):
            self.buttons[y].draw(self.offsetx, self.offsety)

    def highlight(self):
        x, y = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_highlight(x - self.offsetx, y - self.offsety)

    def on_click(self):
        for button in self.buttons:
            button.on_click()


class Cursor:
    def __init__(self, gameField):
        self.carry = ''
        self.cellx = -1
        self.celly = -1
        self.x = -1
        self.y = -1
        self.gameField = gameField

    def process_up(self):
        return

    def process_down(self):
        self.carry, self.gameField.field[self.celly][self.cellx] = (
            self.gameField.field[self.celly][self.cellx],
            self.carry,
        )

    def update_coords(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.cellx, self.celly = min(WIDTH - 1, self.x // BW), min(HEIGHT - 1, self.y // BH)

    def highlight(self):
        draw_square(HIGHLIGHT_COLOUR, self.cellx, self.celly)

    def draw_carry(self):
        if self.carry:
            display.blit(font.render(self.carry, True, BLACK), (self.cellx * BW + 10, self.celly * BW - 8))
