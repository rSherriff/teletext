import numpy as np
import tile_types
import tcod
import xp_loader
import gzip

class Page:
    def __init__(self, file: str):
        xp_file = gzip.open(file)
        raw_data = xp_file.read()
        xp_file.close()

        xp_data = xp_loader.load_xp_string(raw_data)

        self.tiles = np.full((40, 24), fill_value=tile_types.blank, order="F")

        for h in range(0,40):
            for w in range(0,24):
                 self.tiles[h,w]['graphic']=  xp_data['layer_data'][0]['cells'][h][w]
