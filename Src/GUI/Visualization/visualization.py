import pygame

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
    scale as scale_image
from pygame.sprite import \
    OrderedUpdates

from Src.const import ASSETS_PATH, SCREEN_SIZE, FPS, DEBUG
from Src.GUI.Visualization.cow import Cow
from Src.GUI.Visualization.pipe import Pipe

class Visualization:

    screen:Surface
    background:Surface
    sprites:OrderedUpdates
    player:Cow
    inGame:bool

    def __init__(self):       
        self.screen = create_screen(SCREEN_SIZE) 

        self.background = load_image(ASSETS_PATH+"background.png").convert_alpha()
        self.background = scale_image(self.background, SCREEN_SIZE)

        self.screen.blit(self.background, (0,0))
        Pipe.load_images()

        self.inGame = True

        self.player = Cow() 
        self.sprites = OrderedUpdates()
        self.sprites.add(self.player)
        for i in range(100):
            self.sprites.add(Pipe(1000+500*i, self.player))

        if DEBUG:
            print(Pipe.holes)
            print(min(Pipe.holes))
            print(max(Pipe.holes))

        set_screen_caption("Floppy Cow")
        update_screen()

    def play(self):
        
        gameClock = Clock()

        while self.inGame:
            self.handle_events()

            self.sprites.update()
            self.sprites.draw(self.screen)

            update_screen()

            self.sprites.clear(self.screen, self.background)
            
            gameClock.tick(FPS+1)        
        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.inGame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.inGame = False
                if event.key == pygame.K_SPACE:
                    self.player.jump()

if __name__ == "__main__":
    mode = 1
    if(mode==1):
        try:
            game = Game()
            game.play()
        except Exception as e:
            print("======= ERR =======")
            print(e)
            pygame.quit()
    else:
        game = Game()
        game.play()