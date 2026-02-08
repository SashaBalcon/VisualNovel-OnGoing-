import pygame
import sys
import os
from .choice3 import Choice3_1

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx
from save_system.save_ui import SaveUI
from game_state import game_state
from fade_out import FadeOut
from print_text import SlowText

'''
If you select choice 3 (Go to Work), it immediatley goes to this
'''

class C3(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        #save system updates
        UpdateScene('C3')
        UpdateDay1Flags('main_choice', 'go_to_work')

        super().__init__()

        self.scene2_bg = pygame.image.load('day1/day1_anime/frame57.png').convert_alpha()
        self.scene2_bg = pygame.transform.smoothscale(self.scene2_bg, (self.screen_width, self.screen_height))

        self.delay = 1500
        self.delay2 = 2000
        self.space_pressed_once = False
 
        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2]

        self.bg = pygame.Surface((self.text_bar_rect.width, self.text_bar_rect.height), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 150))

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        self.display_text("(Begrudgingly, you decide to follow through and actually go to work. You figure keeping your apartment's more important than a few more hours in bed at the moment.)", color=(255, 255, 255))

         #save system updates
        UpdateTextIdx(self.text_idx)

    def text2(self):
        self.display_text("(Begrudgingly, you decide to follow through and actually go to work. You figure keeping your apartment's more important than a few more hours in bed at the moment.)", color=(255, 255, 255))

         #save system updates
        UpdateTextIdx(self.text_idx)

    def run(self):
        running = True

        self.text_run = True
        self.text_pressed = False
        log_show = False

        self.text_fully_rendered = False

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.scene2_bg, (0, 0))

            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:

                #draw button and text bar ui
                self.draw_buttons()
                
                # words display logic
                if not self.text_fully_rendered:
                    if elapsed > self.delay2 and self.text_run:
                        self.slow_text.update()
                    self.slow_text.Draw(self.screen)

                elif not self.text_pressed:
                    # text fully rendered, waiting for second space press
                    self.slow_text.Draw(self.screen)
                else:
                    # Second space has been pressed — trigger fade
                    if not self.faded:
                        self.fade = FadeOut('day1/day1_anime/frame57.png', 'day1/day1_anime/aquirium.png', self.screen)
                        self.faded = True
                        self.fade.run()

                        scene = C3S2(self.screen)
                        scene.run()
                        return

                #if space bar has been pressed or text bar has been clicked move on to the next line...
                if self.text_pressed:
                    if self.text_idx < len(self.text_funcs):
                        self.text_funcs[self.text_idx]() 
                        self.text_run = True

                if log_show:
                    pygame.draw.rect(self.screen, self.button_color, self.popup)
                    self.back_log_hist()
                    pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                    self.screen.blit(self.x, self.x_text_rect)
                    
                    self.back_log_hist()

                #popup
            if self.popup_visible:
                pygame.draw.rect(self.screen, self.button_color, self.popup)
                pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                self.screen.blit(self.x, self.x_text_rect)

                #exit button
                pygame.draw.rect(self.screen, self.button_color2, self.button_rect)
                self.screen.blit(self.quit_button, self.text_rect_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #If the space key is pressed down skip dailougue loading
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        elif not self.faded:  # second space press
                            self.text_pressed = True  # this will trigger fade

                    #unfull screen mode
                    if event.key in (pygame.K_F11, pygame.K_ESCAPE):
                        game_state.toggle_fullscreen()
                        self.screen = game_state.screen
                        self.width, self.height = game_state.width, game_state.height


                if event.type == pygame.MOUSEBUTTONDOWN:

                #If the text_box is pressed down skip dailougue loading
                    if self.text_bar_rect.collidepoint(mouse):
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        else:
                            self.text_pressed = True
                            self.text_run = True
                            self.text_fully_rendered = False

                    #save button instructions
                    if self.save_rect.collidepoint(mouse):
                        previous_scene = 'C3'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)

            self.clock.tick(60)
            pygame.display.flip()

class C3S2(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('C3S2')

        self.aquirium = pygame.image.load('day1/day1_anime/aquirium.png').convert_alpha()
        self.aquirium = pygame.transform.smoothscale(self.aquirium, (self.screen_width, self.screen_height))

        self.bg = pygame.Surface((self.text_bar_rect.width, self.text_bar_rect.height), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 150))

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4, self.text5, self.text6, self.text7, self.text8]

        self.sammy = self.CharacterSprites("Sammy")

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()

    def text1(self):
        self.display_text("(As you enter your workplace, the aquarium, the familiar scent of cleaning products hits you as you walk through the empty halls. The rows upon rows of glass tanks are lit up on display for your eyes only, with the only other people here shopping at the gift shop that just so happened to stay open. It's Sunday, which means the aquarium is closed, and it's your job to make it ready for the upcoming week. You start by talking with your supervisor and getting your tasks for today.)", color=(255, 255, 255))
        
        #save system updates
        UpdateTextIdx(self.text_idx)
        

    def text2(self):
        self.display_text("(Eventually, you run into Sammy, a coworker and familiar face.)", color = (255, 255, 255))
        
        #save system updates
        UpdateTextIdx(self.text_idx)
    
    def text3(self):
        self.display_text("You: Hey, I didn't know that you worked today.", color = (255, 255, 255))
        
        #save system updates
        UpdateTextIdx(self.text_idx)

    def text4(self):
        self.display_text("Sammy: Yeah I picked up an extra shift. I'll be here on Sundays too from now on. This is your monster shift day right?", color = (173, 113, 217))
        
        #save system updates
        UpdateTextIdx(self.text_idx)

    def text5(self):
        self.display_text("You: Monster shift?", color = (255, 255, 255))
        
        #save system updates
        UpdateTextIdx(self.text_idx)

    def text6(self):
        self.display_text("Sammy: Yeah, the nine-hour-shift block. I saw your schedule on the board in the breakroom.", color = (173, 113, 217))
        
        #save system updates
        UpdateTextIdx(self.text_idx)

    def text7(self):
        self.display_text("You: Ugh. Yeah.", color = (255, 255, 255))
        
        #save system updates
        UpdateTextIdx(self.text_idx)

    def text8(self):
        self.display_text("Sammy: Pfft. Rest in pieces man.", color = (173, 113, 217))


    def run(self):
        running = True

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.aquirium, (0, 0))

            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:

                if self.text_idx >= 2:
                    self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
                    self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47
                    self.screen.blit(self.sammy["neutral_work"], (self.pos_x, self.pos_y))
                if self.text_idx >= 8:
                    self.screen.blit(self.sammy["happy_work"], (self.pos_x, self.pos_y))
        
                #draw button and text bar ui
                self.draw_buttons()
                
                #words
                if elapsed > self.delay2 and text_run:
                    self.slow_text.update()
                self.slow_text.Draw(self.screen)
                if self.text_idx >= len(self.slow_text.text):  
                    self.text_fully_rendered = True
                    text_run = False

                
                #if space bar has been pressed or text bar has been clicked move on to the next line...
                if text_pressed:
                    if self.text_idx < len(self.text_funcs):
                        self.text_funcs[self.text_idx]() 
                        text_run = True
                    else:
                        Choice3_1(self.screen)
                    text_pressed = False

                if log_show:
                    pygame.draw.rect(self.screen, self.button_color, self.popup)
                    self.back_log_hist()
                    pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                    self.screen.blit(self.x, self.x_text_rect)

                #popup
            if self.popup_visible:
                pygame.draw.rect(self.screen, self.button_color, self.popup)
                pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                self.screen.blit(self.x, self.x_text_rect)

                #exit button
                pygame.draw.rect(self.screen, self.button_color2, self.button_rect)
                self.screen.blit(self.quit_button, self.text_rect_button)

            for event in pygame.event.get():

                #If the space key is pressed down skip dailougue loading
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        else:
                            text_pressed = True
                            text_run = True
                            self.text_fully_rendered = False
                    #unfull screen mode
                    if event.key in (pygame.K_F11, pygame.K_ESCAPE):
                        game_state.toggle_fullscreen()
                        self.screen = game_state.screen
                        self.width, self.height = game_state.width, game_state.height


                if event.type == pygame.MOUSEBUTTONDOWN:

                #If the text_box is pressed down skip dailougue loading
                    if self.text_bar_rect.collidepoint(mouse):
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        else:
                            text_pressed = True
                            text_run = True
                            self.text_fully_rendered = False

                    #save button instructions
                    if self.save_rect.collidepoint(mouse):
                        previous_scene = 'C3S2'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)

            self.clock.tick(60)
            pygame.display.flip()
