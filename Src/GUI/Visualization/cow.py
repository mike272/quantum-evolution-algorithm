from pygame import \
    Surface, SRCALPHA
from pygame.image import \
    load as load_image
from pygame.transform import \
    rotate as rotate_image, \
    scale as scale_image
from pygame.sprite import \
    Sprite \

from math import atan
from typing import List
from Src.GUI.Visualization.logic import *

from Src.const import ASSETS_PATH, COW_SIZE, DEBUG, GRAVITY, COW_JUMP_POWER, SCREEN_SIZE, X_VELOCITY, COW_AMPLIFY_ROTATION
from Src.settings import Settings


fitness = 0
closest_pipe = [0,0]

class Cow(Sprite):
    def __init__(self, network: List[Layer], bits: str, settings:Settings):
        Sprite.__init__(self)

        if not settings.silent:
            self.image = load_image(ASSETS_PATH+"cow.png").convert_alpha()
            self.image = scale_image(self.image, COW_SIZE)

            if DEBUG:
                self.image.fill((255,0,0))
        else:
            self.image = Surface(COW_SIZE, SRCALPHA, 32).convert_alpha()
        
        self.image_base = self.image.copy()

        self.bits = bits
        self.rect = self.image.get_rect()
        self.rect_center = self.rect.center
        self.rect.topleft = (100,(SCREEN_SIZE[1]-self.image.get_height())//2)

        self.velocity  = 0
        self.lockJump = False

        self.network = network
        self.settings = settings

        self.fitness = 0
        
    def update(self):
        global fitness, closest_pipe

        if not self.settings.player_controlled:
            if processBits([fitness - closest_pipe[0],
                            self.rect.centery - closest_pipe[1],
                            -self.velocity],
                            self.network, self.settings.quantum):
                self.jump()

        if self.rect.centery<0 or self.rect.centery>=SCREEN_SIZE[1]:
            self.lock()

        self.velocity += GRAVITY
        self.rot_center()

        self.rect.center = (self.rect.centerx, self.rect.centery+self.velocity)


        #if(self.rect.bottom>SCREEN_SIZE[1]): self.jump()

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
        global fitness
        self.velocity = 0
        self.lockJump = True
        self.fitness = self.rect.centerx

    def centerx(self):
        return self.rect.centerx

    def makeRed(self):
        self.image.fill((255,0,0))
        self.image_base.fill((255,0,0))

    @staticmethod
    def fromBits(bits:str, settings:Settings):

        network = initializeNetwork(bits, settings)
        return Cow(network, bits, settings)

    @staticmethod
    def updateStats(f:int, cp:List[int]):
        global fitness, closest_pipe
        fitness = f
        closest_pipe = cp