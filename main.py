import pygame
from pygame.locals import *
import random
from time import time
from config import alph, cons, minv, minc
from menu import *
from config import *

gameField = Field(generate_letters(SEED))
cursor = Cursor(gameField)
gameField.cursor = cursor
ITEM_HEIGHT = BH
menu = Menu([
                Tick("Spellcheck", lambda instance: toggle_spellcheck(gameField, instance), y0=0, state=True),
                Tick("Score Count", lambda instance: toggle_scorecount(gameField, instance), y0=ITEM_HEIGHT, state=True),
                Info(lambda: "Current checkpoint: {}".format(current_checkpoint() + 1), y0=2*ITEM_HEIGHT),
                Button("Checkpoint 1", lambda instance: switch_checkpoint(gameField, 0, instance), y0=3*ITEM_HEIGHT),
                Button("Checkpoint 2", lambda instance: switch_checkpoint(gameField, 1, instance), y0=4*ITEM_HEIGHT),
                Button("Checkpoint 3", lambda instance: switch_checkpoint(gameField, 2, instance), y0=5*ITEM_HEIGHT)
            ],
                A + 100, 200)

curx, cury = 0, 0
registerForEvent(MOUSEBUTTONUP, cursor.process_up)
registerForEvent(MOUSEBUTTONDOWN, menu.on_click)
registerForEvent(MOUSEBUTTONDOWN, cursor.process_down)

while True:
    cursor.update_coords()
    gameField.draw()
    cursor.draw_carry()
    menu.draw()
    tech_pygame()
