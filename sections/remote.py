from sections.section import Section

import numpy as np
import tile_types
import tcod
import xp_loader
import gzip
from ui.remoteUI import RemoteUI
from enum import auto, Enum
from threading import Timer
from playsound import playsound

remote_xp_file = 'images/remote.xp'
num_digits = 3

class RemoteErrors(Enum):
    NONE = auto()
    PAGE_NOT_FOUND = auto()

class Remote(Section):

    def __init__(self, engine, x,y,width, height):
        super().__init__(engine, x, y, width, height)

        xp_file = gzip.open(remote_xp_file)
        raw_data = xp_file.read()
        xp_file.close()

        xp_data = xp_loader.load_xp_string(raw_data)

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.blank, order="F")

        for h in range(0,self.height):
            for w in range(0,self.width):
                 self.tiles[w,h]['graphic']=  xp_data['layer_data'][0]['cells'][w][h]

        self.first_digit_pos = [9,2]
        self.error_message_pos = [4,18]
        self.num_digits = 0
        self.selected_number = [0,0,0]

        self.ui = RemoteUI(self, x,y,self.tiles["graphic"])
        self.remote_error = RemoteErrors.NONE

    def render(self, console):
        super().render(console)

        if self.num_digits > 0:
            console.print(self.x + self.first_digit_pos[0], self.y +  self.first_digit_pos[1], str(self.selected_number[0]), fg=(255,255,255), bg=(0,0,0))
        if self.num_digits > 1:
            console.print(self.x + self.first_digit_pos[0] + 1, self.y +  self.first_digit_pos[1], str(self.selected_number[1]), fg=(255,255,255), bg=(0,0,0))
        if self.num_digits > 2:
            console.print(self.x + self.first_digit_pos[0] + 2, self.y +  self.first_digit_pos[1], str(self.selected_number[2]), fg=(255,255,255), bg=(0,0,0))

        if self.remote_error is RemoteErrors.PAGE_NOT_FOUND:
            console.print(self.x + self.error_message_pos[0], self.y +  self.error_message_pos[1], 'Page not found', fg=(255,0,0), bg=(0,0,0))

    def add_number(self, number : int):
        if self.num_digits == 0:
            if number != 0:
                self.num_digits = 1
                self.selected_number[0] = number
        elif self.num_digits == 1:
            self.num_digits = 2
            self.selected_number[1] = number
        elif self.num_digits == 2:
            self.num_digits = 3
            self.selected_number[2] = number

        playsound("sounds/remote_button_press.wav", False)

    def clear(self):
        for i in range(0, num_digits):
            self.tiles[self.first_digit_pos[0] + i, self.first_digit_pos[1]]['graphic'][0] = ord(' ')

        self.num_digits = 0
        self.selected_number = [0,0,0]

        playsound("sounds/remote_button_press.wav", False)

    def delete_number(self):
        if self.num_digits == 1:
            self.clear()
        elif self.num_digits == 2:
            self.num_digits = 1
            self.selected_number[1] = 0
        elif self.num_digits == 3:
            self.num_digits = 2
            self.selected_number[2] = 0

        playsound("sounds/remote_button_press.wav", False)

    def clear_error(self):
        self.remote_error = RemoteErrors.NONE

    def page_not_found(self):
        self.remote_error = RemoteErrors.PAGE_NOT_FOUND

        playsound("sounds/page_not_found.wav", False)

    def activate(self):
        if self.num_digits == 3:
            page = str((self.selected_number[0] * 100) + (self.selected_number[1] * 10) + self.selected_number[2])
            if self.engine.page_manager.does_page_exist(page):
                self.engine.page_manager.change_page(page)
                self.clear()
            else:
                self.clear()
                for i in range(0,4):
                    if i % 2 == 1:
                        t = Timer(i/2, self.clear_error)
                        t.start()
                    else:
                        t = Timer(i/2, self.page_not_found)
                        t.start()
                        pass