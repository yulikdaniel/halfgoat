import time
from typing import NamedTuple

import pygame
from pydantic import BaseModel, validator
from pygame.locals import QUIT

import checker.new_check as checker


class LettersSettings(BaseModel):
    min_vowel_amt: int
    min_consonant_amt: int
    probability: dict[str, float]
    vowels: list[str]
    consonants: list[str]


class ColoursSettings(BaseModel):
    class Colour(NamedTuple):
        r: int
        g: int
        b: int

    colours_list: dict[str, Colour]

    text_highlight: Colour
    highlight: Colour
    highlight_correct: Colour
    highlight_wrong: Colour
    background: Colour
    tick_box: Colour
    tick_mark: Colour
    text: Colour
    grid: Colour

    @validator(
        "text_highlight",
        "highlight",
        "highlight_correct",
        "highlight_wrong",
        "background",
        "tick_box",
        "tick_mark",
        "text",
        "grid",
        pre=True,
    )
    def validate_colour_name(cls, col_name, values):
        if "colours_list" in values and col_name not in values["colours_list"]:
            raise ValueError(f"colour {col_name} should be in colours list")
        return values["colours_list"][col_name]


class Config(BaseModel):
    letters: LettersSettings
    colours: ColoursSettings
    frames_per_second: int
    ver_cell_amt: int
    hor_cell_amt: int


config = Config.parse_file("config.json")


deliverEvents = dict()


def registerForEvent(type, function, checker=lambda event: True):
    global deliverEvents
    if type not in deliverEvents:
        deliverEvents[type] = []
    deliverEvents[type].append((checker, function))


def clearRegisteredEvents():
    global deliverEvents
    deliverEvents.clear()


class FieldSizes:
    def __init__(self):
        self.update()

    def update_font_size(self):
        sample_size = 100
        sample_let_size = pygame.font.SysFont("comicsansms", sample_size).size("A")
        font_size = self.cell_height / sample_let_size[1] * 0.8 * sample_size
        self.font = pygame.font.SysFont("comicsansms", int(font_size))

    def update(self):
        self.dp_info = pygame.display.Info()
        self.update_font_size()

    @property
    def field_height(self):
        height = min(self.dp_info.current_h, self.dp_info.current_w)
        height -= height % config.ver_cell_amt
        return height

    @property
    def field_width(self):
        width = min(self.dp_info.current_h, self.dp_info.current_w)
        width -= width % config.hor_cell_amt
        return width

    @property
    def cell_height(self):
        return self.field_height // config.ver_cell_amt

    @property
    def cell_width(self):
        return self.field_width // config.hor_cell_amt

    @property
    def menu_width(self):
        return self.dp_info.current_w - self.field_width


checker.build()

iconImg = pygame.image.load("pics/Icon.png")

pygame.init()
pygame.display.set_icon(iconImg)
pygame.display.set_caption("Semigoat")
display = pygame.display.set_mode(flags=pygame.RESIZABLE)
field_sizes = FieldSizes()
clock = pygame.time.Clock()

t1 = 0


def register_general_events():
    registerForEvent(pygame.WINDOWRESIZED, lambda: field_sizes.update())


def tech_pygame():
    global deliverEvents
    global t1
    pygame.display.update()
    display.fill(config.colours.background)
    clock.tick(config.frames_per_second)
    t1 = time.time()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type in deliverEvents:
            for checker, reaction in deliverEvents[event.type]:
                if checker(event):
                    reaction()
