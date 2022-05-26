from pygame import \
    Surface, SRCALPHA
from pygame.image import \
    load as load_image
from pygame.transform import \
    rotate as rotate_image
from pygame.sprite import \
    Sprite \

from math import atan
from random import randint

from Src.const import DEBUG, ASSETS_PATH, HOLE_MIN_DIST, HOLE_SIZE, PIPE_IMAGE_SIZE, SCREEN_SIZE, X_VELOCITY, COW_TOUCH_OFFSET

pipe_up:Surface
pipe_down:Surface

class Pipe(Sprite):
    touched = False
    holes = []
    def __init__(self, pos:int, player:Sprite):
        Sprite.__init__(self)
        self.image = Surface((PIPE_IMAGE_SIZE[0],SCREEN_SIZE[1]), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.hole = randint(HOLE_MIN_DIST+HOLE_SIZE//2,SCREEN_SIZE[1]-HOLE_SIZE//2-HOLE_MIN_DIST)
        if DEBUG:
            Pipe.holes.append(self.hole)
        self.image.blit(pipe_down, (0, -PIPE_IMAGE_SIZE[1]+self.hole-HOLE_SIZE//2))
        self.image.blit(pipe_up, (0, self.hole+HOLE_SIZE//2))
        self.rect.topleft = (pos,0)
        self.player = player

        
    def update(self):
        if not Pipe.touched:
            self.pos-=X_VELOCITY
            self.rect.topleft = (self.pos, 0)

            if abs(self.player.rect.centerx - self.rect.centerx)<=self.player.rect.width\
                and (self.player.rect.top + COW_TOUCH_OFFSET-(self.hole-HOLE_SIZE//2)<=0 
                    or (self.hole+HOLE_SIZE//2) - self.player.rect.bottom + COW_TOUCH_OFFSET<=0):
                        Pipe.touched = True
                        self.player.lock()

    @staticmethod
    def load_images():
        global pipe_down, pipe_up
        pipe_up = load_image(ASSETS_PATH+"pipe_up.png").convert_alpha()
        pipe_down = load_image(ASSETS_PATH+"pipe_down.png").convert_alpha()