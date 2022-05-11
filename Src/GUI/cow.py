from pygame import \
    Surface
from pygame.image import \
    load as load_image
from pygame.transform import \
    rotate as rotate_image, \
    scale as scale_image
from pygame.sprite import \
    Sprite \

from math import atan

from Src.const import ASSETS_PATH, DEBUG, GRAVITY, COW_JUMP_POWER, SCREEN_SIZE, X_VELOCITY, COW_SCALE_DOWN, COW_AMPLIFY_ROTATION

class Cow(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.image = load_image(ASSETS_PATH+"cow.png").convert_alpha()
        self.image = scale_image(self.image, (self.image.get_width()//COW_SCALE_DOWN,self.image.get_height()//COW_SCALE_DOWN))
        if DEBUG:
            self.image.fill((255,0,0))
        
        self.image_base = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect_center = self.rect.center

        self.rect.topleft = (100,(SCREEN_SIZE[1]-self.image.get_height())//2)

        self.velocity  = 0

        self.lockJump = False
        
    def update(self):
        
        self.velocity += GRAVITY
        self.rot_center()

        self.rect.center = (self.rect.centerx, self.rect.centery+self.velocity)
        if(self.rect.bottom>SCREEN_SIZE[1]): self.jump()

    def rot_center(self):
        angle = -COW_AMPLIFY_ROTATION*atan(self.velocity/X_VELOCITY)
        self.image = rotate_image(self.image_base, angle)
        center = self.rect.center
        self.rect = self.image.get_rect(center=self.rect_center)
        self.rect.center = center

    def jump(self):
        if not self.lockJump:
            self.velocity = -COW_JUMP_POWER
    
    def lock(self):
        self.velocity = 0
        self.lockJump = True