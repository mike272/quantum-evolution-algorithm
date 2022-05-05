from pygame.time import \
    Clock
from pygame import \
    Surface
from pygame.display import \
    set_mode as create_screen, \
    set_caption as set_screen_caption, \
    update as update_screen
from pygame.image import \
    load as load_image
from pygame.transform import \
    scale as scale_image, \
    rotate as rotate_image
from pygame.sprite import \
    Sprite, \
    OrderedUpdates

from math import atan,sqrt

from Src.const import ASSETS_PATH, GRAVITY, JUMP_POWER, SCREEN_SIZE, X_VELOCITY

class Cow(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.image = load_image(ASSETS_PATH+"cow.png").convert_alpha()
        self.image_base = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect_center = self.rect.center

        self.rect.topleft = (100,(SCREEN_SIZE[1]-self.image.get_height())//2)

        self.velocity  = 0
        
    def update(self):
        
        self.velocity += GRAVITY
        self.rot_center()

        self.rect.center = (self.rect.centerx, self.rect.centery+self.velocity)
        if(self.rect.bottom>SCREEN_SIZE[1]): self.jump()

    def rot_center(self):
        angle = -8*atan(self.velocity/X_VELOCITY)
        self.image = rotate_image(self.image_base, angle)
        center = self.rect.center
        self.rect = self.image.get_rect(center=self.rect_center)
        self.rect.center = center

    def jump(self):
        self.velocity = -JUMP_POWER
        