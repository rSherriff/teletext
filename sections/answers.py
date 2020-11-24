from sections.section import Section

import numpy as np
import xp_loader
import gzip
import tile_types
from ui.answerUI import AnswersUI

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

        self.ui = AnswersUI(self, x,y, self.tiles["graphic"])
        self.all_answers_correct = False

    def update(self):
        self.all_answers_correct = True
        for answer_input in self.ui.elements:
            if answer_input.input_correct is False:
                self.all_answers_correct = False

        if self.all_answers_correct is True:
            print('All answers correct!')
                

