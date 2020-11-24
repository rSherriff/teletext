from __future__ import annotations

from typing import TYPE_CHECKING

from tcod import Console, event
from highlight import Highlight

import tcod.event
import keyboard
from threading import Timer
from actions.actions import Action, EnterRemoteNumber, ClearRemote, ActivateRemote, CloseMenu, OpenMenu, EscapeAction

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

    def keydown(self, event: tcod.event.KeyDown):
        for element in self.elements:
            element.on_keydown(event)

    def mousedown(self, x: int, y: int):
        for element in self.elements:
            if element.is_mouseover(x, y):
                element.on_mousedown()
            elif isinstance(element, Input):
                element.selected = False
                element.blink = False

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

    def on_keydown(self, event: tcod.event.KeyDown):
        pass

    def is_mouseover(self, x: int, y: int):
        return self.x<= x <= self.x + self.width - 1 and self.y <= y <= self.y + self.height - 1

    def on_mousedown(self):
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
                if self.tiles[w,h][0] != 9488:
                    if self.mouseover:
                        self.tiles[w,h][1] = self.highlight_bg
                    else:
                        self.tiles[w,h][1] = self.normal_bg 

                temp_console.tiles_rgb[h,w] = self.tiles[w,h]
       
        temp_console.blit(console, self.x, self.y)

    def on_mousedown(self):
        self.click_action.perform()

class Input(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x,y,width,height)
        self.selected = False
        self.text = ''
        self.blink_interval = 0.7

    def render(self, console: Console):
        temp_console = Console(width=self.width, height=self.height)
        for w in range(0,self.width):
            if w < len(self.text):
                temp_console.tiles_rgb[0,w] = (ord(self.text[w]), (255,255,255), (0,0,0))

        if self.selected == True:
            if self.blink == True:
                temp_console.tiles_rgb[0,len(self.text)] = (9488, (255,255,255), (0,0,0))

        temp_console.blit(console, self.x, self.y)

    def blink_on(self):
        self.blink = True
        if self.selected == True:
            t = Timer(self.blink_interval, self.blink_off)
            t.start()
    
    def blink_off(self):
        self.blink = False
        if self.selected == True:
            t = Timer(self.blink_interval, self.blink_on)
            t.start()

    def on_mousedown(self):
        self.selected = True
        self.blink_on()

    def on_keydown(self, event):
        if self.selected == True:
            key = event.sym

            if key == tcod.event.K_BACKSPACE:
                self.text = self.text[:-1]
            elif key == tcod.event.K_RETURN or key == tcod.event.K_ESCAPE:
                self.selected = False
                self.blink = False
            elif key == tcod.event.K_SPACE and len(self.text) < self.width - 1:
                self.text += ' '
            elif len(self.text) < self.width - 1:
                letter = get_letter_key(key)
                if keyboard.is_pressed('shift'):
                    letter = letter.capitalize()
                self.text += letter

class CheckedInput(Input):
    def __init__(self, x: int, y: int, width: int, height: int, check_string: str, completion_action: Action):
        super().__init__(x,y,width,height)
        self.check_string = check_string
        self.input_correct = False
        self.completion_action = completion_action

    def on_keydown(self, event):
        super().on_keydown(event)

        if self.text.capitalize() == self.check_string.capitalize():
            self.input_correct = True
            self.completion_action.perform()
        else:
            self.input_correct = False


def get_letter_key(key):
    if key == tcod.event.K_a:
        return 'a'
    elif key == tcod.event.K_b:
        return 'b'
    elif key == tcod.event.K_c:
        return 'c'
    elif key == tcod.event.K_d:
        return 'd'
    elif key == tcod.event.K_e:
        return 'e'
    elif key == tcod.event.K_f:
        return 'f'
    elif key == tcod.event.K_g:
        return 'g'
    elif key == tcod.event.K_h:
        return 'h'
    elif key == tcod.event.K_i:
        return 'i'
    elif key == tcod.event.K_j:
        return 'j'
    elif key == tcod.event.K_k:
        return 'k'
    elif key == tcod.event.K_l:
        return 'l'
    elif key == tcod.event.K_m:
        return 'm'
    elif key == tcod.event.K_n:
        return 'n'
    elif key == tcod.event.K_o:
        return 'o'
    elif key == tcod.event.K_p:
        return 'p'
    elif key == tcod.event.K_q:
        return 'q'
    elif key == tcod.event.K_r:
        return 'r'
    elif key == tcod.event.K_s:
        return 's'
    elif key == tcod.event.K_t:
        return 't'
    elif key == tcod.event.K_u:
        return 'u'
    elif key == tcod.event.K_v:
        return 'v'
    elif key == tcod.event.K_w:
        return 'w'
    elif key == tcod.event.K_x:
        return 'x'
    elif key == tcod.event.K_y:
        return 'y'
    elif key == tcod.event.K_z:
        return 'z'

    return ''