from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
from ui.completeUI import CompleteUI
import os.path

menu_panel_xp_file = 'images/completePanel.xp'

class CompleteSection(Section):
    def __init__(self, engine, x,y,width, height):
        super().__init__(engine, x, y, width, height)

        if os.path.isfile(menu_panel_xp_file):
            xp_file = gzip.open(menu_panel_xp_file)
            raw_data = xp_file.read()
            xp_file.close()

            xp_data = xp_loader.load_xp_string(raw_data)

            self.tiles = np.full((self.width, self.height), fill_value=tile_types.blank, order="F")

            for h in range(0,self.height):
                for w in range(0,self.width):
                    self.tiles[w,h]['graphic']=  xp_data['layer_data'][0]['cells'][w][h]

            self.ui = CompleteUI(self, x,y, self.tiles["graphic"])
