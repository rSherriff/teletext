from sections.page import Page

from datetime import datetime
from enum import auto, Enum
from sections.section import Section

class PageManagerState(Enum):
    DISPLAYING_PAGE = auto()
    SEARCHING_FOR_PAGE = auto()

class PageManager(Section):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine, x, y, width, height)

        self.state= PageManagerState.DISPLAYING_PAGE

        self.pages = {}

        self.pages['100']=Page('images/main.xp')
        self.pages['101']=Page('images/newsMain.xp')
        self.pages['137']=Page('images/test.xp')

        self.active_page_key = '100'
        self.active_page = self.pages[self.active_page_key]

        self.searching_for_page_progress = 100

        self.tiles = self.active_page.tiles

    def render(self, console):
        super().render(console)

        console.tiles_rgb[self.x:self.x+self.width, self.y] = (ord(' '), (0,0,0), (0,0,0))

        console.print(self.x + 3, 0, 'P' + self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        console.print(self.x + 8, 0, 'CEEFAX', fg=(255,255,255), bg=(0,0,0))
        console.print(self.x + 15, 0, '1', fg=(255,255,255), bg=(0,0,0))

        if self.state == PageManagerState.DISPLAYING_PAGE:
            console.print(self.x + 17, 0, self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        elif self.state == PageManagerState.SEARCHING_FOR_PAGE:
            console.print(self.x + 17, 0, str(self.searching_for_page_progress), fg=(255,255,255), bg=(0,0,0))

        now = datetime.now()
        console.print(self.x + 21, 0, now.strftime("%a %d %b"), fg=(255,255,255), bg=(0,0,0))
        console.print(self.x + 32, 0, now.strftime("%H:%M/%S"), fg=(255,255,0), bg=(0,0,0))

    def update(self):
        if self.state == PageManagerState.SEARCHING_FOR_PAGE:
            if str(self.searching_for_page_progress) == self.active_page_key:
                self.state = PageManagerState.DISPLAYING_PAGE
                self.active_page = self.pages[self.active_page_key]
                self.tiles = self.active_page.tiles
            self.searching_for_page_progress += 1

    def change_page(self, page : str):
        if page in self.pages:
            self.active_page_key = page
            self.state = PageManagerState.SEARCHING_FOR_PAGE
            self.searching_for_page_progress = 100
            print('Changing Pages')