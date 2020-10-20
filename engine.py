from __future__ import annotations

import time
from typing import TYPE_CHECKING
import numpy as np

from tcod.console import Console

import tile_types
from input_handlers import EventHandler, MainGameEventHandler
from page_manager import PageManager
from ui import RemoteUI
from remote import Remote


class Engine:
    def __init__(self, screen_width, screen_height, remote_width, remote_height, ui_context_pointer):
       
        self.width = screen_width
        self.height = screen_height
        self.event_handler: EventHandler = MainGameEventHandler(self, ui_context_pointer)
        self.mouse_location = (0, 0)
        self.page_manager = PageManager(self, screen_width, screen_height)
        self.remote = Remote(self, remote_width, remote_height)

        self.remote_ui = RemoteUI(self, self.remote.tiles["graphic"])

    def render(self, root_console: Console, ui_console: Console) -> None:
        """ Renders the game to console. """
        
        self.page_manager.render(root_console)

        self.remote.render(ui_console)
        self.remote_ui.render(ui_console)


    def update(self):
        """ Engine update tick """
        self.page_manager.update()
