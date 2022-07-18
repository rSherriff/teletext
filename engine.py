from __future__ import annotations

import time
from enum import Enum, auto
from threading import Timer
from typing import TYPE_CHECKING

import numpy as np
import tcod
from playsound import playsound
from tcod.console import Console

import tile_types
from effects.melt_effect import MeltWipeEffect, MeltWipeEffectType
from input_handlers import EventHandler, MainGameEventHandler
from sections.answers import Answers
from sections.completion_section import CompleteSection
from sections.menu import Menu
from sections.page_manager import PageManager
from sections.poster import Poster
from sections.remote import Remote

from delta_time import DeltaTime

from application_path import get_app_path


class GameState(Enum):
    MENU = auto()
    IN_GAME = auto()
    COMPLETE = auto()

class Engine:
    def __init__(self):
       
        screen_width = 40
        screen_height = 24

        remote_width = 21
        remote_height = 24

        answer_panel_height = 11

        self.delta_time = DeltaTime()

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.menu = Menu(self, 0,0, screen_width + remote_width,screen_height + answer_panel_height )

        self.page_manager = PageManager(self, 0,0, screen_width, screen_height)
        self.remote_section = Remote(self, screen_width + 1, 0, remote_width, remote_height)
        self.answer_section = Answers(self, 0, screen_height, screen_width + remote_width + 2, answer_panel_height)

        self.full_screen_effect = MeltWipeEffect(self, 0, 0, 64, 35, MeltWipeEffectType.RANDOM, 100)

        #Section Setup
        self.menu_sections = list()
        self.menu_sections.append(self.menu)

        self.game_sections = list()
        self.game_sections.append(self.page_manager)
        self.game_sections.append(self.remote_section)
        #self.game_sections.append(self.answer_section)

        self.completion_sections = list()
        #self.completion_sections.append(CompleteSection(self, 0,0, screen_width + remote_width,screen_height + answer_panel_height))

        self.q1_tooltip = Poster(self,20,15, 28, 11,  get_app_path() +"/images/questionOnePoster.xp")
        self.q2_tooltip = Poster(self,4,18, 28, 8, get_app_path() +"/images/questionFourPoster.xp")
        self.q3_tooltip = Poster(self,4,20, 27, 11, get_app_path() +"/images/questionTwoPoster.xp")
        self.q4_tooltip = Poster(self,33,19, 22, 7, get_app_path() +"/images/questionThreePoster.xp")
        self.q5_tooltip = Poster(self,29,18, 28, 13, get_app_path() +"/images/questionFivePoster.xp")

        self.tooltips = {}
        self.tooltips['q1'] = (self.q1_tooltip)
        self.tooltips['q2'] = (self.q2_tooltip)
        self.tooltips['q3'] = (self.q3_tooltip)
        self.tooltips['q4'] = (self.q4_tooltip)
        self.tooltips['q5'] = (self.q5_tooltip)

        self.completion_criteria = {}
        self.completion_criteria['q1'] = False
        self.completion_criteria['q2'] = False
        self.completion_criteria['q3'] = False
        self.completion_criteria['q4'] = False
        self.completion_criteria['q5'] = False
        self.completion_criteria['q6'] = False

        self.state = GameState.IN_GAME


    def render(self, root_console: Console) -> None:
        """ Renders the game to console """
        for section in self.get_active_sections():
            section.render(root_console)

        if self.state == GameState.IN_GAME:
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

        self.delta_time.update_delta_time()

    def handle_events(self,context: tcod.context.Context):
        self.event_handler.handle_events(context, discard_events=self.full_screen_effect.in_effect)

    def get_active_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections
        elif self.state == GameState.IN_GAME:
            return self.game_sections
        elif self.state == GameState.COMPLETE:
            return self.completion_sections

    def close_menu(self):
        self.state = GameState.IN_GAME
        self.full_screen_effect.start()

    def open_menu(self):
        self.state = GameState.MENU
        self.full_screen_effect.start()

    def complete_game(self):
        self.state = GameState.COMPLETE
        self.full_screen_effect.start()
      
    def correct_answer_given(self, question: str):
        #playsound(get_app_path() +"/sounds/correct_answer.wav", False)
        self.answer_section.answer_correct(question)
        self.completion_criteria[question] = True
        if all(i == True for i in self.completion_criteria.values()):
            self.full_screen_effect.lifespan = 200
            #playsound(get_app_path() + "/sounds/completion_music.wav", False)
            Timer(2, self.complete_game).start()
            

    def show_tooltip(self, key):
        self.tooltips[key].invisible = False

    def hide_tooltip(self, key):
        self.tooltips[key].invisible = True

    def get_delta_time(self):
        return self.delta_time.get_delta_time()
        
