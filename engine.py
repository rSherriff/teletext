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
from sections.poster import Poster

from effects.vertical_wipe_effect import VerticalWipeEffect, VerticalWipeDirection

from playsound import playsound

import tcod

class GameState(Enum):
    MENU = auto()
    IN_GAME = auto()

class Engine:
    def __init__(self):
       
        screen_width = 40
        screen_height = 24

        remote_width = 21
        remote_height = 24

        answer_panel_width = 25
        answer_panel_height = 32

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.menu = Menu(self, 0,0, screen_width + remote_width + answer_panel_width, answer_panel_height)

        self.page_manager = PageManager(self, 0,0, screen_width, screen_height)
        self.remote = Remote(self, screen_width + 1, 0, remote_width, remote_height)
        self.answers = Answers(self, screen_width + remote_width + 1, 0, answer_panel_width, answer_panel_height)

        self.full_screen_effect = VerticalWipeEffect(self, 0, 0, 87, 32)

        #Section Setup
        self.menu_sections = list()
        self.menu_sections.append(self.menu)

        self.game_sections = list()
        self.game_sections.append(self.page_manager)
        self.game_sections.append(self.remote)
        self.game_sections.append(self.answers)

        self.q1_tooltip = Poster(self,50,3, 26, 10, "images/questionOnePoster.xp")
        self.q2_tooltip = Poster(self,50,11, 26, 10, "images/questionFourPoster.xp")
        self.q3_tooltip = Poster(self,50,17, 26, 10, "images/questionTwoPoster.xp")
        self.q4_tooltip = Poster(self,50,15, 26, 7, "images/questionThreePoster.xp")
        self.q5_tooltip = Poster(self,50,14, 26, 12, "images/questionFivePoster.xp")

        self.tooltips = {}
        self.tooltips['q1'] = (self.q1_tooltip)
        self.tooltips['q2'] = (self.q2_tooltip)
        self.tooltips['q3'] = (self.q3_tooltip)
        self.tooltips['q4'] = (self.q4_tooltip)
        self.tooltips['q5'] = (self.q5_tooltip)

        self.state = GameState.MENU


    def render(self, root_console: Console) -> None:
        """ Renders the game to console """
        for section in self.get_active_sections():
            section.render(root_console)

        for tooltip in self.tooltips.values():
            tooltip.render(root_console)

        if self.full_screen_effect.in_effect == True:
            self.full_screen_effect.render(root_console)
        else:
            self.full_screen_effect.set_tiles(root_console.tiles_rgb)


    def update(self):
        """ Engine update tick """
        for section in self.get_active_sections():
            section.update()

    def handle_events(self,context: tcod.context.Context):
        self.event_handler.handle_events(context, discard_events=self.full_screen_effect.in_effect)

    def get_active_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections
        elif self.state == GameState.IN_GAME:
            return self.game_sections

    def close_menu(self):
        self.state = GameState.IN_GAME
        self.full_screen_effect.start(VerticalWipeDirection.DOWN)

    def open_menu(self):
        self.state = GameState.MENU
        self.full_screen_effect.start(VerticalWipeDirection.UP)
      
    def correct_answer_given(self, answer_number):
        playsound("sounds/correct_answer.wav", False)
        print("Correct answer given for question {0}".format(answer_number))

    def show_tooltip(self, key):
        self.tooltips[key].invisible = False

    def hide_tooltip(self, key):
        self.tooltips[key].invisible = True
        
