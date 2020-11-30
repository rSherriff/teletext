from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
from ui.answerUI import AnswersUI

from effects.horizontal_wipe_effect import HorizontalWipeEffect, HorizontalWipeDirection

answer_panel_xp_file = 'images/answerPanel.xp'

class Answers(Section):
    def __init__(self, engine, x,y,width, height):
        super().__init__(engine, x, y, width, height)

        xp_file = gzip.open(answer_panel_xp_file)
        raw_data = xp_file.read()
        xp_file.close()

        xp_data = xp_loader.load_xp_string(raw_data)

        self.tiles = np.full((self.width, self.height), fill_value=tile_types.blank, order="F")

        for h in range(0,self.height):
            for w in range(0,self.width):
                self.tiles[w,h]['graphic']=  xp_data['layer_data'][0]['cells'][w][h]

        self.correct_colour = (0,255,0)

        self.ui = AnswersUI(self, x,y, self.tiles["graphic"], self.correct_colour)
        self.all_answers_correct = False

        """
        self.answer_areas = {}
        self.answer_areas['q1'] = (3, 4, 16, 1)

        self.effects = {}
        self.effects['q1'] = HorizontalWipeEffect(self, 3, 4, 16, 1)
        """

    def render(self, root_console):
        super().render(root_console)

        """
        for effect in self.effects.values():
            if effect.in_effect == True:
                effect.render(root_console)
            else:
                effect.set_tiles(root_console.tiles_rgb[effect.x : effect.x + effect.width, effect.y: effect.y + effect.height])
        """


    def answer_correct(self, question : str):
        #self.effects[question].start(HorizontalWipeDirection.LEFT)
        #self.tiles[self.effects[question].x : self.effects[question].x + self.effects[question].width, self.effects[question].y: self.effects[question].y + self.effects[question].height]['graphic']['bg'] = self.correct_colour
        pass