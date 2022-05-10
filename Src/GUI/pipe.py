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

from Src.const import ASSETS_PATH, GRAVITY, HOLE_MIN_DIST, HOLE_SIZE, JUMP_POWER, PIPE_IMAGE_SIZE, SCREEN_SIZE, X_VELOCITY

pipe_up:Surface
pipe_down:Surface

class Pipe(Sprite):
    touched = False
    def __init__(self, pos:int, player:Sprite):
        Sprite.__init__(self)
        self.image = Surface((PIPE_IMAGE_SIZE[0],SCREEN_SIZE[1]), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.hole = randint(HOLE_MIN_DIST+HOLE_SIZE,SCREEN_SIZE[1]-HOLE_SIZE-HOLE_MIN_DIST)
        self.image.blit(pipe_down, (0, -PIPE_IMAGE_SIZE[1]+self.hole-HOLE_SIZE//2))
        self.image.blit(pipe_up, (0, self.hole+HOLE_SIZE//2))
        self.rect.topleft = (pos,0)
        self.player = player

        
    def update(self):
        if not Pipe.touched:
            self.pos-=X_VELOCITY
            self.rect.topleft = (self.pos, 0)

        if abs(self.player.rect.centerx - self.rect.centerx)<=200\
            and abs(self.player.rect.centery-self.hole)>=HOLE_SIZE:
                Pipe.touched = True
                self.player.lock()

    @staticmethod
    def load_images():
        global pipe_down, pipe_up
        pipe_up = load_image(ASSETS_PATH+"pipe_up.png").convert_alpha()
        pipe_down = load_image(ASSETS_PATH+"pipe_down.png").convert_alpha()