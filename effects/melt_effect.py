from effects.effect import Effect

from tcod import Console
from enum import auto, Enum
from random import randrange

import numpy as np

class MeltWipeEffectType(Enum):
    WAVE_LEFT = auto()
    WAVE_RIGHT = auto()
    RANDOM = auto()

class MeltWipeEffect(Effect):
    def __init__(self, engine, x, y, width, height, type: MeltWipeEffectType):
        super().__init__(engine,x,y,width,height)
        
        self.lifespan = 25
        self.type = type

        self.col_trigger_times = np.empty(width)
        for col in range(0,self.width):
            wave_step = 0.25
            if self.type == MeltWipeEffectType.WAVE_LEFT:
                self.col_trigger_times[col] = wave_step * col
            elif self.type == MeltWipeEffectType.WAVE_RIGHT:
                self.col_trigger_times[-col - 1] = wave_step * col
            elif self.type == MeltWipeEffectType.RANDOM:
                self.col_trigger_times[col] = wave_step * randrange(30)
        
    def start(self):
        super().start()
        self.current_wipe_heights = np.empty(self.width)
        self.current_wipe_heights.fill(0)
        
    def render(self, console):
        if self.time_alive > self.lifespan:
            self.stop()

        
        for col in range(0, self.width):

            if self.time_alive > self.col_trigger_times[col]:
                self.current_wipe_heights[col] += 0.5

            temp_console = Console(width=1, height=self.height, order="F")

            for y in range(0, self.height):
                temp_console.tiles_rgb[0,y] = self.tiles[col,y]

            temp_console.blit(console, src_x=0, src_y=0,
                                        dest_x=col, dest_y= int(self.current_wipe_heights[col]), 
                                        width=1, height=self.height - int(self.current_wipe_heights[col]))
        self.time_alive += 0.16