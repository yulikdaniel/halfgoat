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


class SizeConstants:
    def __init__(self):
        self.update()

    def update_font_size(self):
        sample_size = 100
        sample_let_size = pygame.font.SysFont("comicsansms", sample_size).size("A")
        font_size = self.BH / sample_let_size[1] * 0.8 * sample_size
        self.font = pygame.font.SysFont("comicsansms", int(font_size))

    def update(self):
        self.WIDTH = 20
        self.HEIGHT = 20
        info = pygame.display.Info()
        self.A = min(info.current_h, info.current_w)
        self.B = self.A
        self.A -= self.A % self.WIDTH
        self.B -= self.B % self.HEIGHT
        self.BW = self.A // self.WIDTH
        self.BH = self.B // self.HEIGHT
        self.MENUWIDTH = info.current_w - self.B
        self.update_font_size()


checker.build()

iconImg = pygame.image.load("pics/Icon.png")

pygame.init()
pygame.display.set_icon(iconImg)
pygame.display.set_caption("Semigoat")
display = pygame.display.set_mode(flags=pygame.RESIZABLE)
CONSTANTS = SizeConstants()
clock = pygame.time.Clock()

t1 = 0


def register_general_events():
    registerForEvent(pygame.WINDOWRESIZED, lambda: CONSTANTS.update())


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
