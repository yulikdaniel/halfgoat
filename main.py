from pygame.locals import *
import random
from menu import *
from config import *


def launch_game(SEED):
    clearRegisteredEvents()
    gameField = Field(generate_letters(SEED))
    cursor = Cursor(gameField)
    gameField.cursor = cursor
    ITEM_HEIGHT = BH
    menu = Menu([
        Tick("Spellcheck", lambda instance: toggle_spellcheck(
            gameField, instance), y0=0, state=True),
        Tick("Score Count", lambda instance: toggle_scorecount(
            gameField, instance), y0=ITEM_HEIGHT, state=True),
        Info(lambda: "Current checkpoint: {}".format(
            current_checkpoint() + 1), y0=2*ITEM_HEIGHT),
        Button("Checkpoint 1", lambda instance: switch_checkpoint(
            gameField, 0, instance), y0=3*ITEM_HEIGHT),
        Button("Checkpoint 2", lambda instance: switch_checkpoint(
            gameField, 1, instance), y0=4*ITEM_HEIGHT),
        Button("Checkpoint 3", lambda instance: switch_checkpoint(
            gameField, 2, instance), y0=5*ITEM_HEIGHT)
    ],
        A + 100, 200)

    registerForEvent(MOUSEBUTTONUP, cursor.process_up)
    registerForEvent(MOUSEBUTTONDOWN, menu.on_click)
    registerForEvent(MOUSEBUTTONDOWN, cursor.process_down)

    while True:
        tech_pygame()
        cursor.update_coords()
        gameField.draw()
        cursor.draw_carry()
        menu.draw()


SEED = 0


def start_menu():
    def func(symbol):
        global SEED
        if symbol == -1:
            SEED //= 10
        elif symbol == -2:
            launch_game(random.randint(0, 10**9) if SEED == 0 else SEED)
        else:
            SEED = 10 * SEED + symbol

    clearRegisteredEvents()
    ITEM_HEIGHT = BH
    menu = Menu([
        Info(lambda: "Enter seed: {}".format(
            SEED if SEED else "random"), y0=ITEM_HEIGHT),
        Button("Launch game", lambda: launch_game(random.randint(
            0, 10**9) if SEED == 0 else SEED), y0=2*ITEM_HEIGHT)
    ],
        0, 0)
    for i in range(10):
        registerForEvent(KEYDOWN, lambda i=i: func(
            i), lambda event, i=i: event.unicode == str(i))
    registerForEvent(KEYDOWN, lambda: func(-1),
                     lambda event: event.key == K_BACKSPACE)
    registerForEvent(KEYDOWN, lambda: func(-2),
                     lambda event: event.key == K_RETURN)
    registerForEvent(MOUSEBUTTONDOWN, menu.on_click)
    while True:
        tech_pygame()
        menu.draw()


start_menu()
