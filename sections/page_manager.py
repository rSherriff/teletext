from sections.page import Page

from datetime import datetime
from enum import auto, Enum
from sections.section import Section
from playsound import playsound
from application_path import get_app_path
from threading import Timer

class PageManagerState(Enum):
    DISPLAYING_PAGE = auto()
    SEARCHING_FOR_PAGE = auto()

class RemoteErrors(Enum):
    NONE = auto()
    PAGE_NOT_FOUND = auto()

class PageManager(Section):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine, x, y, width, height)

        self.state= PageManagerState.DISPLAYING_PAGE

        self.pages = {}

        self.pages['100']=Page('/images/main.xp')
        self.pages['101']=Page('/images/newsMain.xp')
        self.pages['102']=Page('/images/102.xp')
        self.pages['103']=Page('/images/103.xp')
        self.pages['104']=Page('/images/104.xp')
        self.pages['105']=Page('/images/105.xp')
        self.pages['106']=Page('/images/106.xp')
        self.pages['107']=Page('/images/107.xp')
        self.pages['115']=Page('/images/weatherMain.xp')
        self.pages['116']=Page('/images/weatherMap.xp')
        self.pages['120']=Page('/images/120.xp')

        self.pages['201']=Page('/images/sportsMain.xp')
        self.pages['202']=Page('/images/202.xp')
        self.pages['203']=Page('/images/203.xp')
        self.pages['204']=Page('/images/204.xp')

        self.pages['301']=Page('/images/musicMain.xp')
        self.pages['302']=Page('/images/302.xp')
        self.pages['303']=Page('/images/303.xp')
        self.pages['304']=Page('/images/304.xp')
        self.pages['310']=Page('/images/310.xp')
        self.pages['311']=Page('/images/311.xp')
        self.pages['312']=Page('/images/312.xp')
        self.pages['313']=Page('/images/313.xp')
        self.pages['320']=Page('/images/320.xp')
        self.pages['330']=Page('/images/330.xp')

        self.pages['401']=Page('/images/tvMain.xp')
        self.pages['402']=Page('/images/402.xp')
        self.pages['403']=Page('/images/403.xp')
        self.pages['404']=Page('/images/404.xp')
        self.pages['405']=Page('/images/405.xp')
        self.pages['406']=Page('/images/406.xp')
        self.pages['501']=Page('/images/letters.xp')
        self.pages['601']=Page('/images/gangway.xp')
        
        self.active_page_key = '100'
        self.active_page = self.pages[self.active_page_key]
        self.page_change_speed = 100
        self.searching_for_page_progress = 100

        self.tiles = self.active_page.tiles
        self.num_digits = 0
        self.selected_number = [0,0,0]
        self.remote_error = RemoteErrors.NONE

    def render(self, console):
        super().render(console)

        console.tiles_rgb[self.x:self.x+self.width, self.y] = (ord(' '), (0,0,0), (0,0,0))

        if self.num_digits > 0:
            console.print(self.x + 2, 0, str(self.selected_number[0]), fg=(255,255,255), bg=(0,0,0))
        if self.num_digits > 1:
            console.print(self.x + 3, 0, str(self.selected_number[1]), fg=(255,255,255), bg=(0,0,0))
        if self.num_digits > 2:
            console.print(self.x + 4, 0, str(self.selected_number[2]), fg=(255,255,255), bg=(0,0,0))

        if self.remote_error is RemoteErrors.PAGE_NOT_FOUND:
            console.print(self.x, self.y, 'NO PAGE', fg=(255,0,0), bg=(0,0,0))

        console.print(self.x + 7, 0, 'TELUSFAX', fg=(255,255,255), bg=(0,0,0))

        if self.state == PageManagerState.DISPLAYING_PAGE:
            console.print(self.x + 16, 0, self.active_page_key, fg=(255,255,255), bg=(0,0,0))
        elif self.state == PageManagerState.SEARCHING_FOR_PAGE:
            console.print(self.x + 16, 0, str(int(self.searching_for_page_progress)), fg=(255,255,255), bg=(0,0,0))

        now = datetime.now()
        console.print(self.x + 20, 0, now.strftime("%a %d %b"), fg=(255,255,255), bg=(0,0,0))
        console.print(self.x + 31, 0, now.strftime("%H:%M/%S"), fg=(255,255,0), bg=(0,0,0))

    def update(self):
        if self.state == PageManagerState.SEARCHING_FOR_PAGE:
            if self.searching_for_page_progress >= int(self.active_page_key):
                self.state = PageManagerState.DISPLAYING_PAGE
                self.active_page = self.pages[self.active_page_key]
                self.tiles = self.active_page.tiles
                playsound(get_app_path() + "/sounds/arrive_at_page.wav", False)
            self.searching_for_page_progress += max(self.page_change_speed * self.engine.get_delta_time(), 1)

    def change_page(self, page : str):
        if page in self.pages:
            self.active_page_key = page
            self.state = PageManagerState.SEARCHING_FOR_PAGE
            self.searching_for_page_progress = 100
            playsound(get_app_path() + "/sounds/search.wav", False)

    def does_page_exist(self, page : str):
        return page in self.pages

    def add_number(self, number : int):
        if self.num_digits == 0:
            if number != 0:
                self.num_digits = 1
                self.selected_number[0] = number
        elif self.num_digits == 1:
            self.num_digits = 2
            self.selected_number[1] = number
        elif self.num_digits == 2:
            self.num_digits = 3
            self.selected_number[2] = number

        if self.num_digits == 3:
            self.activate()

        #playsound(get_app_path() + "/sounds/remote_button_press.wav", False)

    def clear(self):
        for i in range(0, self.num_digits):
            self.tiles[2 + i, 0]['graphic'][0] = ord(' ')

        self.num_digits = 0
        self.selected_number = [0,0,0]

    def delete_number(self):
        if self.num_digits == 1:
            self.clear()
        elif self.num_digits == 2:
            self.num_digits = 1
            self.selected_number[1] = 0
        elif self.num_digits == 3:
            self.num_digits = 2
            self.selected_number[2] = 0

        playsound(get_app_path() + "/sounds/remote_button_press.wav", False)

    def clear_error(self):
        self.remote_error = RemoteErrors.NONE

    def page_not_found(self):
        self.remote_error = RemoteErrors.PAGE_NOT_FOUND
        playsound(get_app_path() + "/sounds/page_not_found.wav", False)

    def activate(self):
        if self.num_digits == 3:
            page = str((self.selected_number[0] * 100) + (self.selected_number[1] * 10) + self.selected_number[2])
            if self.does_page_exist(page):
                self.change_page(page)
                t = Timer(1, self.clear).start()
            else:
                self.clear()
                for i in range(0,4):
                    if i % 2 == 1:
                        t = Timer(i/2, self.clear_error).start()
                    else:
                        t = Timer(i/2, self.page_not_found).start()
                        pass