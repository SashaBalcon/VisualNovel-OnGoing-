import pygame
import sys
import os
from .c1 import C1
from .c2 import C2_Choice
from .c3 import C3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx
from save_system.save_ui import SaveUI
from game_state import game_state

class Choice1_1(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen
        self.text_idx = text_idx

        super().__init__()

        #save system updates
        UpdateScene('Choice1_1')

        self.scene2_bg = pygame.image.load('day1/day1_anime/frame57.png').convert_alpha()
        self.scene2_bg = pygame.transform.smoothscale(self.scene2_bg, (self.screen_width, self.screen_height))

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(script_dir, ".."))
        self.font_path = os.path.join(project_dir, "Fonts", "ArchitectsDaughter-Regular.ttf")

        self.choice_font = pygame.font.Font(self.font_path, 23)
        self.white = (255, 255, 255)

        self.RecMain()
        self.run()

    def RecMain(self):
        #Pop up Bar
        self.bg = pygame.Surface((self.screen_width, 300), pygame.SRCALPHA) 
        self.bg.fill((0, 0, 0, 150)) 

        self.text_bar_rect = self.bg.get_rect()
        self.text_bar_rect.center = (self.screen_width // 2, self.screen_height // 2)

        #choice1
        self.choice1 = self.choice_font.render('Stay at Home', True, self.white)

        #square surrounding choice1
        self.choice1_rect = pygame.Rect(0, 0, 500, 32)
        self.choice1_rect.centerx = self.text_bar_rect.centerx
        self.choice1_rect.centery = self.text_bar_rect.centery - 40
        self.choice1_rect2 = self.choice1.get_rect(center = self.choice1_rect.center)

        #choice2
        self.choice2 = self.choice_font.render('Hang out with friends', True, self.white)

        #square surrounding choice2
        self.choice2_rect = pygame.Rect(0, 0, 500, 32)
        self.choice2_rect.centerx = self.text_bar_rect.centerx
        self.choice2_rect.centery = self.text_bar_rect.centery
        self.choice2_rect2 = self.choice2.get_rect(center = self.choice2_rect.center)

        #choice3
        self.choice3 = self.choice_font.render('Go to Work', True, self.white)

        #square surrounding choice3
        self.choice3_rect = pygame.Rect(0, 0, 500, 32)
        self.choice3_rect.centerx = self.text_bar_rect.centerx
        self.choice3_rect.centery = self.text_bar_rect.centery + 40
        self.choice3_rect2 = self.choice3.get_rect(center = self.choice3_rect.center)

    def run(self):
        running = True

        while running:
            mouse = pygame.mouse.get_pos()

            #background
            self.screen.blit(self.scene2_bg, (0, 0))

            #choice pop up screen
            self.screen.blit(self.bg, self.text_bar_rect)

            #choices 1, 2, and 3
            pygame.draw.rect(self.screen, self.button_color2, self.choice1_rect)
            pygame.draw.rect(self.screen, self.button_color2, self.choice2_rect)
            pygame.draw.rect(self.screen, self.button_color2, self.choice3_rect)

            self.screen.blit(self.choice1, self.choice1_rect2)
            self.screen.blit(self.choice2, self.choice2_rect2)
            self.screen.blit(self.choice3, self.choice3_rect2)

            #exit button
            pygame.draw.rect(self.screen, self.button_color2, self.button_rect2)
            self.screen.blit(self.quit_button2, self.text_rect_button2)

            #save button
            pygame.draw.rect(self.screen, self.button_color2, self.save_rect2)
            self.screen.blit(self.save_button_surface2, self.text_save_rect2)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    #unfull screen mode
                    if event.key in (pygame.K_F11, pygame.K_ESCAPE):
                        game_state.toggle_fullscreen()
                        self.screen = game_state.screen
                        self.width, self.height = game_state.width, game_state.height

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect2.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

                    if self.save_rect2.collidepoint(mouse):
                        previous_scene = 'Choice1_1'
                        save_screen = SaveUI(self.screen, previous_scene, 1)
                        save_screen.run()
                    
                    #choice1
                    if self.choice1_rect.collidepoint(mouse):
                        C1(self.screen)
                        running = False

                    #choice2
                    if self.choice2_rect.collidepoint(mouse):
                         C2_Choice(self.screen)
                         running = False

                    #choice3
                    if self.choice3_rect.collidepoint(mouse):
                        C3(self.screen)
                        running = False

            pygame.display.flip()

    '''
    Source:
    https://www.geeksforgeeks.org/python-match-case-statement/
    '''