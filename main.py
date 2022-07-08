import random

from pygame.locals import *

from config import *
from menu import *


def launch_game(SEED):
    clearRegisteredEvents()
    register_general_events()
    gameField = Field(generate_letters(SEED))
    cursor = Cursor(gameField)
    gameField.cursor = cursor
    menu = Menu(
        [
            Tick("Spellcheck", lambda instance: toggle_spellcheck(gameField, instance), y0=lambda: 0, state=True),
            Tick(
                "Score Count",
                lambda instance: toggle_scorecount(gameField, instance),
                y0=lambda: field_sizes.cell_height,
                state=True,
            ),
            Info(lambda: "Current checkpoint: {}".format(current_checkpoint() + 1), y0=lambda: 2 * field_sizes.cell_height),
            Button(
                "Checkpoint 1", lambda instance: switch_checkpoint(gameField, 0, instance), y0=lambda: 3 * field_sizes.cell_height
            ),
            Button(
                "Checkpoint 2", lambda instance: switch_checkpoint(gameField, 1, instance), y0=lambda: 4 * field_sizes.cell_height
            ),
            Button(
                "Checkpoint 3", lambda instance: switch_checkpoint(gameField, 2, instance), y0=lambda: 5 * field_sizes.cell_height
            ),
        ],
        lambda: field_sizes.field_height + field_sizes.cell_height * 2,
        lambda: 200 + field_sizes.cell_width * 2,
    )

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
    register_general_events()
    menu = Menu(
        [
            Info(lambda: "Enter seed: {}".format(SEED if SEED else "random"), y0=lambda: field_sizes.cell_height),
            Button(
                "Launch game",
                lambda instance: launch_game(random.randint(0, 10**9) if SEED == 0 else SEED),
                y0=lambda: 2 * field_sizes.cell_height,
            ),
        ],
        lambda: 0,
        lambda: 0,
    )
    for i in range(10):
        registerForEvent(KEYDOWN, lambda i=i: func(i), lambda event, i=i: event.unicode == str(i))
    registerForEvent(KEYDOWN, lambda: func(-1), lambda event: event.key == K_BACKSPACE)
    registerForEvent(KEYDOWN, lambda: func(-2), lambda event: event.key == K_RETURN)
    registerForEvent(MOUSEBUTTONDOWN, menu.on_click)
    while True:
        tech_pygame()
        menu.draw()


start_menu()
