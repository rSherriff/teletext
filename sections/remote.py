from sections.section import Section

import numpy as np
import tile_types
import tcod
import xp_loader
import gzip
from ui import RemoteUI

remote_xp_file = 'images/remote.xp'
num_digits = 3

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
        self.num_digits = 0
        self.selected_number = 0

        self.ui = RemoteUI(self, x,y,self.tiles["graphic"])

    def add_number(self, number : int):
        if self.num_digits == 0:
            self.num_digits = 1
            self.selected_number = number * 100
            self.tiles[self.first_digit_pos[0], self.first_digit_pos[1]]['graphic'][0] = number + 48
            self.tiles[self.first_digit_pos[0], self.first_digit_pos[1]]['graphic'][1] = (255,255,255)
        elif self.num_digits == 1:
            self.num_digits = 2
            self.selected_number += number * 10
            self.tiles[self.first_digit_pos[0] + 1, self.first_digit_pos[1]]['graphic'][0] = number + 48
            self.tiles[self.first_digit_pos[0] + 1, self.first_digit_pos[1]]['graphic'][1] = (255,255,255)
        elif self.num_digits == 2:
            self.num_digits = 3
            self.selected_number += number
            self.tiles[self.first_digit_pos[0] + 2, self.first_digit_pos[1]]['graphic'][0] = number + 48
            self.tiles[self.first_digit_pos[0] + 2, self.first_digit_pos[1]]['graphic'][1] = (255,255,255)

    def clear(self):
        for i in range(0, num_digits):
            self.tiles[self.first_digit_pos[0] + i, self.first_digit_pos[1]]['graphic'][0] = ord(' ')

        self.num_digits = 0
        self.selected_number = 0

    def activate(self):
        self.engine.page_manager.change_page(str(self.selected_number))
        self.clear()
