import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx, UpdatePoints
from save_system.save_ui import SaveUI
from game_state import game_state
from print_text import SlowText

class C3C12C12C12C12C2(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('C3C12C12C12C12C2')

        self.aquirium = pygame.image.load('day1/day1_anime/aquirium.png').convert_alpha()
        self.aquirium = pygame.transform.smoothscale(self.aquirium, (self.screen_width, self.screen_height))

        self.night = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.night = pygame.transform.smoothscale(self.night, (self.screen_width, self.screen_height))

        self.bg = pygame.Surface((self.text_bar_rect.width, self.text_bar_rect.height), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 150))

        self.mary = pygame.image.load('day1/day1_anime/mary.png').convert_alpha()

        original_rect = self.mary.get_rect()
        desired_width = 1500
        aspect_ratio = original_rect.height / original_rect.width
        desired_height = int(desired_width * aspect_ratio)

        self.mary = pygame.transform.smoothscale(self.mary, (desired_width, desired_height))
        self.show_mary = False

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = 0
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4, self.text5, self.text6, self.text7]

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.sammy = self.CharacterSprites("Sammy")
        self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
        self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(Sammy lets out a little chuckle.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text2(self):
        text = "Sammy: You know what? Fair enough."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text3(self):
        text = " (Sammy glances over at the unstocked shelf and turns back to face you as if giving you a hint.) "

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text4(self):
        text = "Sammy: Ok, really though, see you around?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text5(self):
        text = "You: Yeah, see you."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text6(self):
        text = "(You go back to work and do so until your shift is over. Eventually, the end of the day comes. You didn't get to finish all your tasks, but that's a problem for the next shift worker to deal with.) "

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text7(self):
        text = "(Right now, you're tired, and the embrace of your bed is all you can think of. Eventually, you get home and rest up for the next day.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def run(self):
        running = True
        played_animation = False

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        self.screen.blit(self.aquirium, (0, 0))

        if self.text_idx >= 6:
                self.screen.blit(self.night, (0, 0))

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.aquirium, (0, 0))

            if self.text_idx < 4:
                self.screen.blit(self.sammy["happy_work"], (self.pos_x, self.pos_y))
            elif self.text_idx <= 6:
                self.screen.blit(self.sammy["neutral_work"], (self.pos_x, self.pos_y))

            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:
        
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
                        pass
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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
                    if self.save_rect2.collidepoint(mouse):
                        previous_scene = 'C3C12C12C12C12C2'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)

            self.clock.tick(60)
            pygame.display.flip()

