from __future__ import annotations

import time
from typing import TYPE_CHECKING
import numpy as np

from tcod.console import Console

import tile_types
from input_handlers import EventHandler, MainGameEventHandler
from sections.page_manager import PageManager
from sections.remote import Remote
from sections.answers import Answers

class Engine:
    def __init__(self):
       
        screen_width = 40
        screen_height = 24

        remote_width = 21
        remote_height = 24

        answer_panel_width = 26
        answer_panel_height = 32

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.page_manager = PageManager(self, 0,0, screen_width, screen_height)
        self.remote = Remote(self, screen_width + 1, 0, remote_width, remote_height)
        self.answers = Answers(self, screen_width + remote_width + 1, 0, answer_panel_width, answer_panel_height)

        #Section Setup
        self.sections = list()
        self.sections.append(self.page_manager)
        self.sections.append(self.remote)
        self.sections.append(self.answers)

    def render(self, root_console: Console) -> None:
        """ Renders the game to console. """
        for section in self.sections:
            section.render(root_console)

    def update(self):
        """ Engine update tick """
        for section in self.sections:
            section.update()
