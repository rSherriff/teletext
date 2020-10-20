#!/usr/bin/env python3
import copy
import time

import tcod

from engine import Engine
from tcod.sdl import Window


def main() -> None:
    root_width = 40
    root_height = 24

    ui_width = 20
    ui_height = 18

    tileset = tcod.tileset.load_tilesheet(
        "./ceefax_teletext_6x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )


    with tcod.context.new_terminal(
        root_width,
        root_height,
        tileset=tileset,
        title="Teletext",
        vsync=True,
        #sdl_window_flags = tcod.context.SDL_WINDOW_BORDERLESS
    ) as root_context:
        root_console = tcod.Console(root_width, root_height, order="F")
        
        root_window = Window(root_context.sdl_window_p)
        root_window.position = [700,400]

        with tcod.context.new_terminal(
            ui_width,
            ui_height,
            tileset=tileset,
            title="Teletext",
            vsync=True,
            #sdl_window_flags = tcod.context.SDL_WINDOW_BORDERLESS
        ) as ui_context:

            ui_console = tcod.Console(ui_width, ui_height, order="F")
            ui_window = Window(ui_context.sdl_window_p)
            ui_window.position = [1000,500]

            engine = Engine(root_width, root_height, ui_width, ui_height, ui_context.sdl_window_p)

            cycle = 0
            while True:
                root_console.clear()
                ui_console.clear()

                engine.event_handler.on_render(root_console=root_console, ui_console=ui_console)

                root_context.present(root_console)
                ui_context.present(ui_console)

                #engine.event_handler.handle_events(root_context)
                engine.event_handler.handle_events(ui_context)

                cycle += 1
                if cycle % 15 == 0:
                    engine.update()

if __name__ == "__main__":
    main()