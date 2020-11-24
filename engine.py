from __future__ import annotations

import time
from enum import Enum, auto
from typing import TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types
from input_handlers import EventHandler, MainGameEventHandler
from sections.answers import Answers
from sections.menu import Menu
from sections.page_manager import PageManager
from sections.remote import Remote

class GameState(Enum):
    MENU = auto()
    IN_GAME = auto()

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

        self.menu = Menu(self, 0,0, screen_width + remote_width + answer_panel_width, answer_panel_height)

        self.page_manager = PageManager(self, 0,0, screen_width, screen_height)
        self.remote = Remote(self, screen_width + 1, 0, remote_width, remote_height)
        self.answers = Answers(self, screen_width + remote_width + 1, 0, answer_panel_width, answer_panel_height)

        #Section Setup
        self.menu_sections = list()
        self.menu_sections.append(self.menu)

        self.game_sections = list()
        self.game_sections.append(self.page_manager)
        self.game_sections.append(self.remote)
        self.game_sections.append(self.answers)

        self.state = GameState.MENU

    def render(self, root_console: Console) -> None:
        """ Renders the game to console. """
        for section in self.get_active_sections():
            section.render(root_console)
       

    def update(self):
        """ Engine update tick """
        for section in self.get_active_sections():
            section.update()

    def get_active_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections
        elif self.state == GameState.IN_GAME:
            return self.game_sections

    def close_menu(self):
        self.state = GameState.IN_GAME

    def open_menu(self):
        self.state = GameState.MENU

    def correct_answer_given(self, answer_number):
        print("Correct answer given for question {0}".format(answer_number))
        
