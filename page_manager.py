from page import Page

from datetime import datetime
from enum import auto, Enum

class PageManagerState(Enum):
    DISPLAYING_PAGE = auto()
    SEARCHING_FOR_PAGE = auto()

class PageManager:
    def __init__(self, engine, width, height):
        self.engine = engine
        self.width = width
        self.height = height
        self.state= PageManagerState.DISPLAYING_PAGE

        self.pages = {}

        self.pages['100']=Page('./test.xp')
        self.pages['121']=Page('./test.xp')
        self.pages['137']=Page('./test.xp')

        self.active_page_key = '100'
        self.active_page = self.pages[self.active_page_key]

        self.searching_for_page_progress = 100

    def render(self, console):
        console.tiles_rgb[0: self.width, 0: self.height] = self.active_page.tiles["graphic"]

        console.tiles_rgb[0:self.width, 0] = (ord(' '), (0,0,0), (0,0,0))
        console.print(3, 0, 'P' + self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        console.print(8, 0, 'CEEFAX', fg=(255,255,255), bg=(0,0,0))
        console.print(15, 0, '1', fg=(255,255,255), bg=(0,0,0))

        if self.state == PageManagerState.DISPLAYING_PAGE:
            console.print(17, 0, self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        elif self.state == PageManagerState.SEARCHING_FOR_PAGE:
            console.print(17, 0, str(self.searching_for_page_progress), fg=(255,255,255), bg=(0,0,0))

        now = datetime.now()
        console.print(21, 0, now.strftime("%a %d %b"), fg=(255,255,255), bg=(0,0,0))
        console.print(32, 0, now.strftime("%H:%M/%S"), fg=(255,255,0), bg=(0,0,0))

    def update(self):
        if self.state == PageManagerState.SEARCHING_FOR_PAGE:
            self.searching_for_page_progress += 1
            if str(self.searching_for_page_progress) == self.active_page_key:
                self.state = PageManagerState.DISPLAYING_PAGE
                self.active_page = self.pages[self.active_page_key]

    def change_page(self, page : str):
        if page in self.pages:
            self.active_page_key = page
            self.state = PageManagerState.SEARCHING_FOR_PAGE
            self.searching_for_page_progress = 100
            print('Changing Pages')