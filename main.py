#!/usr/bin/env python3
import copy
import time

import tcod

from engine import Engine
from tcod.sdl import Window


def main() -> None:
    screen_width = 88
    screen_height = 30

    tileset = tcod.tileset.load_tilesheet(
        "./ceefax_teletext_6x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    with tcod.context.new_terminal(
        screen_width * 2,
        screen_height * 2,
        tileset=tileset,
        title="Teletext",
        vsync=True,
        sdl_window_flags = tcod.context.SDL_WINDOW_BORDERLESS
    ) as root_context:

        root_console = tcod.Console(screen_width, screen_height, order="F")
        engine = Engine()

        cycle = 0
        while True:
            root_console.clear()

            engine.event_handler.on_render(root_console=root_console)

            root_context.present(root_console)

            engine.event_handler.handle_events(root_context)

            cycle += 1
            if cycle % 2 == 0:
                engine.update()

if __name__ == "__main__":
    main()