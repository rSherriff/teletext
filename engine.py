from __future__ import annotations

import time
from typing import TYPE_CHECKING
import numpy as np

from tcod.console import Console

import tile_types
from input_handlers import EventHandler, MainGameEventHandler
from sections.page_manager import PageManager
from sections.remote import Remote


class Engine:
    def __init__(self):
       
        screen_width = 40
        screen_height = 24

        remote_width = 21
        remote_height = 24

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        #Section Setup
        self.page_manager = PageManager(self, 0,0, screen_width, screen_height)
        self.remote = Remote(self, screen_width + 1, 0, remote_width, remote_height)

    def render(self, root_console: Console) -> None:
        """ Renders the game to console. """
        
        self.page_manager.render(root_console)
        self.remote.render(root_console)


    def update(self):
        """ Engine update tick """
        self.page_manager.update()
