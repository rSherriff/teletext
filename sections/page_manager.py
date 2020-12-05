from sections.page import Page

from datetime import datetime
from enum import auto, Enum
from sections.section import Section
from playsound import playsound

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
        self.pages['102']=Page('images/102.xp')
        self.pages['103']=Page('images/103.xp')
        self.pages['104']=Page('images/104.xp')
        self.pages['105']=Page('images/105.xp')
        self.pages['106']=Page('images/106.xp')
        self.pages['107']=Page('images/107.xp')
        self.pages['115']=Page('images/weatherMain.xp')
        self.pages['116']=Page('images/weatherMap.xp')
        self.pages['120']=Page('images/120.xp')

        self.pages['201']=Page('images/sportsMain.xp')
        self.pages['202']=Page('images/202.xp')
        self.pages['203']=Page('images/203.xp')
        self.pages['204']=Page('images/204.xp')

        self.pages['301']=Page('images/musicMain.xp')
        self.pages['303']=Page('images/303.xp')
        self.pages['304']=Page('images/304.xp')
        self.pages['305']=Page('images/305.xp')
        self.pages['310']=Page('images/310.xp')
        self.pages['320']=Page('images/320.xp')
        self.pages['330']=Page('images/330.xp')

        self.pages['401']=Page('images/tvMain.xp')
        self.pages['402']=Page('images/402.xp')
        self.pages['403']=Page('images/403.xp')
        self.pages['404']=Page('images/404.xp')
        self.pages['405']=Page('images/405.xp')
        self.pages['406']=Page('images/406.xp')
        self.pages['501']=Page('images/letters.xp')
        self.pages['601']=Page('images/judyProgram.xp')
        
        self.active_page_key = '100'
        self.active_page = self.pages[self.active_page_key]

        self.searching_for_page_progress = 100

        self.tiles = self.active_page.tiles

    def render(self, console):
        super().render(console)

        console.tiles_rgb[self.x:self.x+self.width, self.y] = (ord(' '), (0,0,0), (0,0,0))

        console.print(self.x + 3, 0, 'P' + self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        console.print(self.x + 8, 0, 'TELUSFAX', fg=(255,255,255), bg=(0,0,0))

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
                playsound("sounds/arrive_at_page.wav", False)
            self.searching_for_page_progress += 1

    def change_page(self, page : str):
        if page in self.pages:
            self.active_page_key = page
            self.state = PageManagerState.SEARCHING_FOR_PAGE
            self.searching_for_page_progress = 100
            playsound("sounds/search.wav", False)

    def does_page_exist(self, page : str):
        return page in self.pages