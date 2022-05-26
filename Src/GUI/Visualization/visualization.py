import pygame
from typing import List

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
from Src.GUI.Visualization.logic import *

from Src.const import ASSETS_PATH, PIPE_DIST, SCREEN_SIZE, FPS
from Src.GUI.Visualization.cow import Cow
from Src.GUI.Visualization.pipe import Pipe
from Src.settings import Settings

class Visualization:

    screen:Surface
    background:Surface
    sprites_player:OrderedUpdates
    players:List[Cow]
    silent:bool
    inGame:bool

    def __init__(self, players:List[str] , settings:Settings):   

        self.settings = settings
        self.silent = settings.silent

        self.screen = create_screen(SCREEN_SIZE)

        if not self.silent:    

            self.background = load_image(ASSETS_PATH+"background.png").convert_alpha()
            self.background = scale_image(self.background, SCREEN_SIZE)

            self.screen.blit(self.background, (0,0))
            Pipe.load_images()

        self.inGame = True

        self.players:List[Cow] = [0]*len(players)
        for i in range(0,len(players)):
            self.players[i] = Cow.fromBits(players[i], self.settings)

        self.pipes:List[Pipe] = [0]*100
        for i in range(100):
            self.pipes[i] = Pipe(PIPE_DIST*(i+1), self.players, self.settings)

        self.sprites_player = OrderedUpdates()
        self.sprites_player.add(self.players)

        self.sprites_pipes = OrderedUpdates()
        self.sprites_pipes.add(self.pipes)

        set_screen_caption("Floppy Cow")
        update_screen()

    def play(self):
        global fitness
        gameClock = Clock()

        
        while self.inGame:
            self.handle_events()

            try:
                test_player = self.sprites_player.sprites()[0]
            except: 
                self.players = self.sort(self.players)
                self.players = self.breed(self.players, self.settings)
                self.sprites_player.add(self.players)
                self.sprites_pipes.remove(self.pipes)

                for pipe in self.pipes: 
                    pipe.reset(self.players)

                self.sprites_pipes.add(self.pipes)

                test_player = self.sprites_player.sprites()[0]


            
            try:
                closest_pipe = self.sprites_pipes.sprites()[0]

                Cow.updateStats(test_player.centerx(), closest_pipe.centertop())

                self.sprites_player.update()
                self.sprites_player.draw(self.screen)

                self.sprites_pipes.update()
                self.sprites_pipes.draw(self.screen)

                for player in self.players:
                    if player.lockJump:
                        self.sprites_player.remove(player)

                for pipe in self.pipes:
                    if pipe.rect.centerx<test_player.rect.left:
                        self.sprites_pipes.remove(pipe)
                update_screen()

                self.sprites_player.clear(self.screen, self.background)
                self.sprites_pipes.clear(self.screen, self.background)

                gameClock.tick(FPS+1)        
            except:
                self.inGame = False

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
                    for player in self.players:
                        player.jump()

    def sort(self, players:List[Cow]):
        return sorted(players, key = lambda cow:cow.fitness, reverse = True)

    def breed(self, players:List[Cow], settings: Settings):
        champs = [p.bits for p in players[0:settings.leaders_count]]
        players = [0]*settings.babies_count
        c = 0
        for i in range(0, len(champs)):
            players[i] = Cow.fromBits(champs[i], settings)

        for i in range(len(champs), settings.babies_count):
            players[i] = Cow.fromBits(randomBits(champs[c%len(champs)], settings.mutation_rate), settings)
            c+=1

        return players 

if __name__ == "__main__":
    mode = 1
    settings = Settings()
    bits = [settings.initial_bits]

    if(mode==1):
        try:
            game = Visualization(bits, settings)
            game.play()
        except Exception as e:
            print("======= ERR =======")
            print(e)
            pygame.quit()
    else:
        game = Visualization(bits, settings)
        game.play()