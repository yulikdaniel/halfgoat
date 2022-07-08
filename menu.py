import pygame

from config import *
from field import *


class Tick:
    def __init__(self, text, effect, x0=lambda: 0, y0=lambda: 0, state=False):
        self.text = text
        self.effect = effect
        self.state = state
        self.highlight = False
        self.y = y0
        self.x = x0

    def draw(self, offsetx, offsety):
        offsetx += self.x()
        offsety += self.y()
        pygame.draw.rect(
            display,
            config.colours.tick_box,
            (offsetx, offsety - 0.2 * field_sizes.cell_height, field_sizes.cell_width, field_sizes.cell_height),
            width=3,
        )
        if self.highlight:
            pygame.draw.rect(
                display,
                config.colours.highlight,
                (offsetx, offsety - 0.2 * field_sizes.cell_height, field_sizes.cell_width, field_sizes.cell_height),
                width=0,
            )
        if self.state:
            pygame.draw.line(
                display,
                config.colours.tick_mark,
                (offsetx + 0.2 * field_sizes.cell_width, offsety + 0.1 * field_sizes.cell_height),
                (offsetx + field_sizes.cell_width / 2, offsety + field_sizes.cell_height * 0.7),
                width=4,
            )
            pygame.draw.line(
                display,
                config.colours.tick_mark,
                (offsetx + field_sizes.cell_width / 2, offsety + field_sizes.cell_height * 0.7),
                (offsetx + field_sizes.cell_width * 0.8, offsety),
                width=4,
            )
        display.blit(
            field_sizes.font.render(self.text, True, config.colours.text),
            (offsetx + field_sizes.cell_width * 1.2, offsety),
        )

    def check_highlight(self, pos_x, pos_y):
        if (
            self.x() <= pos_x <= self.x() + field_sizes.cell_width
            and self.y() <= pos_y + 0.2 * field_sizes.cell_height <= self.y() + field_sizes.cell_height
        ):
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        if self.highlight:
            self.effect(self)


class Button:
    def __init__(self, text, effect, x0=lambda: 0, y0=lambda: 0):
        self.text = text
        self.effect = effect
        self.highlight = False
        self.y = y0
        self.x = x0
        self.texts = [
            lambda: field_sizes.font.render(self.text, True, config.colours.text),
            lambda: field_sizes.font.render(self.text, True, config.colours.text_highlight),
        ]

    def draw(self, offsetx, offsety):
        display.blit(self.texts[self.highlight](), (self.x() + offsetx, self.y() + offsety))

    def check_highlight(self, pos_x, pos_y):
        if (
            self.x() <= pos_x <= self.x() + self.texts[self.highlight]().get_width()
            and self.y() <= pos_y <= self.y() + self.texts[self.highlight]().get_height()
        ):
            self.highlight = True
        else:
            self.highlight = False

    def on_click(self):
        if self.highlight:
            self.effect(self)


class Info:
    def __init__(self, getText, x0=lambda: 0, y0=lambda: 0):
        self.highlight = False
        self.y = y0
        self.x = x0
        self.getText = lambda: field_sizes.font.render(
            getText if isinstance(getText, str) else getText(), True, config.colours.text
        )

    def draw(self, offsetx, offsety):
        display.blit(self.getText(), (self.x() + offsetx, self.y() + offsety))

    def check_highlight(self, pos_x, pos_y):
        if (
            self.x() <= pos_x <= self.x() + self.getText().get_width()
            and self.y() <= pos_y <= self.y() + self.getText().get_height()
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
            self.buttons[y].draw(self.offsetx(), self.offsety())

    def highlight(self):
        x, y = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_highlight(x - self.offsetx(), y - self.offsety())

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
        self.cellx, self.celly = min(config.hor_cell_amt - 1, self.x // field_sizes.cell_width), min(
            config.ver_cell_amt - 1, self.y // field_sizes.cell_height
        )

    def highlight(self):
        draw_square(config.colours.highlight, self.cellx, self.celly)

    def draw_carry(self):
        if self.carry:
            display.blit(
                field_sizes.font.render(self.carry, True, config.colours.text),
                ((self.cellx + 0.1) * field_sizes.cell_width, (self.celly - 0.1) * field_sizes.cell_height),
            )
