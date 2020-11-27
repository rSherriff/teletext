from effects.effect import Effect

from tcod import Console
from enum import auto, Enum

class VerticalWipeDirection(Enum):
    UP = auto()
    DOWN = auto()

class VerticalWipeEffect(Effect):
    def __init__(self, engine, x, y, width, height):
        super().__init__(engine,x,y,width,height)
        self.current_wipe_height = 0
        
    def start(self, direction: VerticalWipeDirection):
        super().start()
        self.direction = direction
        self.current_wipe_height = 0
        
    def render(self, console):
        if self.time_alive > self.lifespan:
            self.stop()
        
        if(self.direction == VerticalWipeDirection.DOWN):
            self.current_wipe_height += 0.7
        elif(self.direction == VerticalWipeDirection.UP):
            self.current_wipe_height -= 0.7

        temp_console = Console(width=self.width, height=self.height, order="F")

        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                temp_console.tiles_rgb[x,y] = self.tiles[x,y]

        temp_console.blit(console, src_x=self.x, src_y=self.y , dest_x=0, dest_y=0 + int(self.current_wipe_height), width=self.width, height=self.height - int(self.current_wipe_height))

        self.time_alive += 0.16