from ui.ui import UI
from ui.ui import Button

from actions.actions import ClearRemote, EnterRemoteNumber, ActivateRemote, OpenMenu

import tcod.event

class RemoteUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [6, 4,3,3] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 1), tiles=button_tiles )
        self.add_element(one_button)

        bd = [9,4,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        two_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 2), tiles=button_tiles )
        self.add_element(two_button)

        bd = [12,4,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        three_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 3), tiles=button_tiles )
        self.add_element(three_button)

        bd = [6,7,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        four_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 4), tiles=button_tiles )
        self.add_element(four_button)

        bd = [9,7,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        five_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 5), tiles=button_tiles )
        self.add_element(five_button)

        bd = [12,7,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        six_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 6), tiles=button_tiles )
        self.add_element(six_button)

        bd = [6,10,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        seven_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 7), tiles=button_tiles )
        self.add_element(seven_button)

        bd = [9,10,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        eight_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 8), tiles=button_tiles )
        self.add_element(eight_button)

        bd = [12,10,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        nine_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 9), tiles=button_tiles )
        self.add_element(nine_button)

        bd = [6,13,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        clear_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=ClearRemote(self.section.engine), tiles=button_tiles )
        self.add_element(clear_button)

        bd = [9,13,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        zero_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnterRemoteNumber(self.section.engine, 0), tiles=button_tiles )
        self.add_element(zero_button)

        bd = [12,13,3,3]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        go_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=ActivateRemote(self.section.engine), tiles=button_tiles )
        self.add_element(go_button)

    def keydown(self, event: tcod.event.KeyDown):
        super().keydown(event)
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            OpenMenu(self.section.engine).perform()
        