import pygame
import sys
import os
from .c3c12c12c12c12c2 import C3C12C12C12C12C2
from .slug_liar import SlugLiar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx, UpdatePoints
from save_system.save_ui import SaveUI
from game_state import game_state
from print_text import SlowText

class C3C12C12C12C12C1(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('C3C12C12C12C12C1')

        self.aquirium = pygame.image.load('day1/day1_anime/aquirium.png').convert_alpha()
        self.aquirium = pygame.transform.smoothscale(self.aquirium, (self.screen_width, self.screen_height))

        self.bg2 = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.bg2 = pygame.transform.smoothscale(self.bg2, (self.screen_width, self.screen_height))

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

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2]

        self.sammy = self.CharacterSprites("Sammy")

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(She stares at you quizzically, almost surprised you gave that answer.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text2(self):
        text = "Sammy: Yeah? What do you like about it then?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def run(self):
        running = True
        played_animation = False

        text_run = True
        text_pressed = False
        log_show = False

        self.screen.blit(self.aquirium, (0, 0))

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.aquirium, (0, 0))

            if self.text_idx <= 2:
                self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
                self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47
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
                elif text_run == False:
                    self.slow_text.update()
                    self.slow_text.Draw(self.screen)
                
                #if space bar has been pressed or text bar has been clicked move on to the next line...
                if text_pressed:
                    if self.text_idx < len(self.text_funcs):
                        self.text_funcs[self.text_idx]() 
                        text_run = True
                    else:
                        extra_choice(self.screen)
                        running = False
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
                        self.slow_text.UpdateFast()
                        text_pressed = True
                        text_run = False

                    #unfull screen mode
                    if event.key in (pygame.K_F11, pygame.K_ESCAPE):
                        game_state.toggle_fullscreen()
                        self.screen = game_state.screen
                        self.width, self.height = game_state.width, game_state.height

                if event.type == pygame.MOUSEBUTTONDOWN:

                #If the text_box is pressed down skip dailougue loading
                    if self.text_bar_rect.collidepoint(mouse):
                        self.slow_text.UpdateFast()
                        text_pressed = True
                        text_run = False

                    #save button instructions
                    if self.save_rect.collidepoint(mouse):
                        previous_scene = 'C3C12C12C12C12C1'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)
                    
            self.clock.tick(60)
            pygame.display.flip()

class extra_choice(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen
        super().__init__()

        #save system updates
        UpdateScene('extra_choice')

        self.scene2_bg = pygame.image.load('day1/day1_anime/aquirium.png').convert_alpha()
        self.scene2_bg = pygame.transform.smoothscale(self.scene2_bg, (self.screen_width, self.screen_height))

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(script_dir, ".."))
        self.font_path = os.path.join(project_dir, "Fonts", "ArchitectsDaughter-Regular.ttf")

        self.choice_font = pygame.font.Font(self.font_path,23)
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
        self.choice1 = self.choice_font.render('Working with sea creatures is just really cool.', True, self.white)

        #square surrounding choice1
        self.choice1_rect = pygame.Rect(0, 0, 500, 32)
        self.choice1_rect.centerx = self.text_bar_rect.centerx
        self.choice1_rect.centery = self.text_bar_rect.centery - 40
        self.choice1_rect2 = self.choice1.get_rect(center = self.choice1_rect.center)

        #choice2
        self.choice2 = self.choice_font.render("The pay.", True, self.white)

        #square surrounding choice2
        self.choice2_rect = pygame.Rect(0, 0, 500, 32)
        self.choice2_rect.centerx = self.text_bar_rect.centerx
        self.choice2_rect.centery = self.text_bar_rect.centery
        self.choice2_rect2 = self.choice2.get_rect(center = self.choice2_rect.center)

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

            self.screen.blit(self.choice1, self.choice1_rect2)
            self.screen.blit(self.choice2, self.choice2_rect2)

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect2.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

                    if self.save_rect2.collidepoint(mouse):
                        previous_scene = 'extra_choice'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()
                    
                    #choice1
                    if self.choice1_rect.collidepoint(mouse):
                        sea_slugs(self.screen)
                        running = False

                    #choice2
                    if self.choice2_rect.collidepoint(mouse):
                         C3C12C12C12C12C2(self.screen)
                         running = False

            pygame.display.flip()


class sea_slugs(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

         #save system updates
        UpdateScene('sea_slugs')

        self.aquirium = pygame.image.load('day1/day1_anime/aquirium.png').convert_alpha()
        self.aquirium = pygame.transform.smoothscale(self.aquirium, (self.screen_width, self.screen_height))

        self.bg2 = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.bg2 = pygame.transform.smoothscale(self.bg2, (self.screen_width, self.screen_height))

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

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4, self.text5, self.text6, self.text7, self.text8]

        self.sammy = self.CharacterSprites("Sammy")

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "You: Sometimes I just find myself staring at the tanks I clean. I was at the sea slug tank the other day-"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text2(self):
        text = "Sammy: Wait, we have one of those?!"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))
    
    def text3(self):
        text = "You: Yeah, over in-"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        
    def text4(self):
        text = "Sammy: Take me there. Now."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))
    
    def text5(self):
        text = "(You head over to the tank of nudibranch. They seem… humble. They don't do much - you wouldn't even know if they were alive - yet Sammy seems completely infatuated with them. Seconds, minutes go by, and Sammy hasn't said a single word.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text6(self):
        text = "You: Uhhh, Sammy?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text7(self):
        text = "Sammy: Yeah, yeah, yeah shut up a second."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text8(self):
        text = " (You observe as one slightly twitches. Fantastic.) "

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

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.aquirium, (0, 0))

            if self.text_idx < 3:
                self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
                self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47
                self.screen.blit(self.sammy["neutral_work"], (self.pos_x, self.pos_y))
            elif self.text_idx >= 3:
                self.screen.blit(self.sammy["excited_work"], (self.pos_x, self.pos_y))
    

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
                        SlugLiar(self.screen)
                        running = False
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
                    if self.save_rect.collidepoint(mouse):
                        previous_scene = 'sea_slugs'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)

            self.clock.tick(60)
            pygame.display.flip()

