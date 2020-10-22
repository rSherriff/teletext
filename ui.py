from __future__ import annotations

from typing import TYPE_CHECKING

from tcod import Console, event
from highlight import Highlight

from actions import Action, EnterRemoteNumber, ClearRemote, ActivateRemote

class UI:
    def __init__(self, section, x, y):
        self.elements = list()
        self.highlight = Highlight()

        self.x = x
        self.y = y
        self.section = section

    def render(self, console: Console):
        for element in self.elements:
            element.render(console)

        if self.highlight is not None:
            self.highlight.render(console)
            pass

    def mousedown(self, x: int, y: int):
        for element in self.elements:
            if element.is_mouseover(x, y):
                if isinstance(element, Button):
                    element.click_action.perform()

    def mousemove(self, x: int, y: int):
        for element in self.elements:
            if element.is_mouseover(x, y):
                element.mouseover = True
            else:
                element.mouseover = False

    def add_element(self, element):
        element.x = element.x + self.x
        element.y = element.y + self.y
        self.elements.append(element)

class RemoteUI(UI):
     def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()
        self.highlight = Highlight()

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
        

class UIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mouseover = False
        pass

    def render(self):
        raise NotImplementedError()

    def is_mouseover(self, x: int, y: int) -> bool:
        raise NotImplementedError()


class Button(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int, click_action: Action, tiles):
        super().__init__(x,y,width,height)
        self.click_action = click_action
        self.tiles = tiles

        self.highlight_bg = (128,128,128)
        self.normal_bg= (255,255,255)

    def render(self, console: Console):
        temp_console = Console(self.width, self.height)

        for w in range(0,self.width):
            for h in range(0, self.height):
                if self.tiles[h,w][0] != 9488:
                    if self.mouseover:
                        self.tiles[h,w][1] = self.highlight_bg
                    else:
                        self.tiles[h,w][1] = self.normal_bg 

                temp_console.tiles_rgb[w,h] = self.tiles[h,w]
       
        temp_console.blit(console, self.x, self.y)

    def is_mouseover(self, x: int, y: int):
        return self.x<= x <= self.x + self.width - 1 and self.y <= y <= self.y + self.height - 1
