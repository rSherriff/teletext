from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
from ui.menuUI import MenuUI
import os.path

menu_panel_xp_file = 'images/menuPanel'


class Menu(Section):
    def __init__(self, engine, x,y,width, height):
        super().__init__(engine, x, y, width, height)

        self.animated_tiles =list()
        for i in range(0,3):
            if os.path.isfile(menu_panel_xp_file  + str(i+1) + '.xp'):
                xp_file = gzip.open(menu_panel_xp_file  + str(i+1)+ '.xp')
                raw_data = xp_file.read()
                xp_file.close()

                xp_data = xp_loader.load_xp_string(raw_data)

                self.animated_tiles.append(np.full((self.width, self.height), fill_value=tile_types.blank, order="F"))

                for h in range(0,self.height):
                    for w in range(0,self.width):
                        self.animated_tiles[i][w,h]['graphic']=  xp_data['layer_data'][0]['cells'][w][h]

        self.ui = MenuUI(self, x,y, self.animated_tiles[0]["graphic"])
        self.selected_tiles = 0
        self.frame_length = 20
        self.time_on_frame =0

    def render(self, console):
        if self.time_on_frame > self.frame_length:
            self.selected_tiles += 1
            self.selected_tiles %= 3
            self.time_on_frame = 0

        if len(self.animated_tiles[self.selected_tiles]) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.animated_tiles[self.selected_tiles]["graphic"]

            if self.ui is not None:
                self.ui.render(console)

        self.time_on_frame += 0.16
