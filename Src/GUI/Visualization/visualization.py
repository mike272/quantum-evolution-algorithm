from cv2 import bitwise_and
import matplotlib.pylab as plt
import pygame
from typing import Dict, List

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

from Src.const import *
from Src.settings import Settings

class Visualization:

    screen:Surface
    background:Surface
    sprites_player:OrderedUpdates
    players:List[Cow]
    silent:bool
    inGame:bool

    def __init__(self, players_bits:List[str] , settings:Settings):   

        self.settings = settings
        self.silent = settings.silent

        self.screen = create_screen(SCREEN_SIZE)

        self.background = load_image(ASSETS_PATH+"background.png").convert_alpha()
        self.background = scale_image(self.background, SCREEN_SIZE)
        
        self.screen.blit(self.background, (0,0))
        
        Pipe.load_images()
        self.inGame = True
        self.fpsLock = True

        self.players:List[Cow] = makeCows(players_bits, settings)
        self.sprites_player = OrderedUpdates(self.players)

        self.pipes:List[Pipe]  = makePipes(self.sprites_player, settings)
        self.sprites_pipes = OrderedUpdates(self.pipes)

        set_screen_caption("Floppy Cow")
        update_screen()

    def play(self):
        gameClock = Clock()

        fitness = 0
        pipes_passed = 0

        epochs_passed = 0
        while self.inGame:
            self.handle_events()

            if(len(self.sprites_player.sprites())==0):
                fitness = 0
                pipes_passed = 0
                epochs_passed+=1

                if epochs_passed==10:
                    self.silent = False

                self.players = list(sorted(self.players, key = lambda cow:cow.fitness, reverse = True))
                self.players = breed(self.players, self.settings)
                self.sprites_player.add(self.players)

                self.sprites_pipes.empty()
                for pipe in self.pipes: pipe.reset()
                self.sprites_pipes.add(self.pipes)

                

            
            if(len(self.sprites_pipes.sprites())!=0):
                
                closest_pipe = self.sprites_pipes.sprites()[0]
                Cow.updateStats(fitness, closest_pipe.data(), pipes_passed*PIPE_IMAGE_SIZE[0])

                self.sprites_player.update()
                self.sprites_pipes.update()
                
                if not self.silent: 
                    self.sprites_player.draw(self.screen)
                    self.sprites_pipes.draw(self.screen)


                for player in self.sprites_player.sprites():
                    if player.lockJump:
                        self.sprites_player.remove(player)
                        print(f"Remaining: {len(self.sprites_player.sprites())}")

                for pipe in self.sprites_pipes.sprites():
                    if pipe.rect.centerx<COW_X - COW_SIZE[0]//2:
                        self.sprites_pipes.remove(pipe)
                        pipes_passed += 1
                        print(f"Pipes left: {self.settings.pipes-pipes_passed}")

                if not self.silent: 
                    update_screen()

                    self.sprites_player.clear(self.screen, self.background)
                    self.sprites_pipes.clear(self.screen, self.background)

                    if self.fpsLock:
                        gameClock.tick(FPS+1)
                    else:
                        gameClock.tick()
                else:
                    gameClock.tick()
                set_screen_caption(f"Floppy Cow {round(gameClock.get_fps(),1)}")    
                fitness+=1    
            else:
                if(len(self.sprites_player.sprites())<40 and False):
                    fitness = 0
                    pipes_passed = 0
                    epochs_passed+=1

                    self.players = list(sorted(self.players, key = lambda cow:cow.fitness, reverse = True))
                    self.players = breed(self.players, self.settings)
                    self.sprites_player.add(self.players)

                    self.sprites_pipes.empty()
                    for pipe in self.pipes: pipe.reset()
                    self.sprites_pipes.add(self.pipes)
                    continue

                self.inGame = False
                bits_dict:Dict[int, Dict[str, int]] = {}

                for player in self.sprites_player.sprites():
                    bits_arr = [''.join(x) for x in zip(*[iter(player.bits)]*self.settings.float_precision)]
                    for idx,bit in enumerate(bits_arr):

                        if idx in bits_dict.keys():
                            if bit in bits_dict[idx]:
                                bits_dict[idx][bit] += 1
                            else:
                                bits_dict[idx][bit] = 1
                        else:
                            bits_dict[idx] = {bit:1}
                        
                labels = [f"{int(key)+1} gene" for key in bits_dict.keys()]
                rows = list(set([key for dicts in bits_dict.values() for key in dicts.keys()]))
                vals = [val for dicts in bits_dict.values() for val in dicts.values()]
                colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))

                cell_text = []

                for r in rows:
                    cell_text_data = []
                    for key,data in bits_dict.items():
                        cell_text_data.append(data[r] if r in data.keys() else 0)
                    cell_text.append(cell_text_data)

                fig, ax = plt.subplots()
                ax.xaxis.set_visible(False) 
                ax.yaxis.set_visible(False)

                table = plt.table(
                        cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=labels,

                        loc='top')

                plt.subplots_adjust(left=0.1, bottom=0.1)
                #plt.title('Most frequent gene by gene nr')
                plt.show()
        pygame.quit()

    

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.inGame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.inGame = False
                    print("Quit simulation")
                if event.key == pygame.K_SPACE:
                    for player in self.players:
                        player.jump()
                    print(f"All players jump")
                if event.key == pygame.K_s:
                    self.silent = not self.silent
                    print(f"Visualization rendering: {not self.silent}")

                if event.key == pygame.K_x:
                    if(len(self.sprites_player.sprites()) == 0): return
                    for player in self.players:
                        if not player.lockJump:
                            player.lock()
                            self.sprites_player.remove(player)
                            print(f"Killed (first in sprites) alive player")
                            print(f"Remaining: {len(self.sprites_player.sprites())}")
                            break
                if event.key == pygame.K_a:
                    self.fpsLock = not self.fpsLock
                    print(f"FPS lock: {self.fpsLock}")

    
