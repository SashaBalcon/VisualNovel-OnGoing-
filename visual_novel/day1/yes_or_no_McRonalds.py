import pygame
import sys
import os

from .start_mary_convo import StartMaryConvo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx, UpdatePoints
from save_system.save_ui import SaveUI
from game_state import game_state
from print_text import SlowText

class YesOrNo(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen
        super().__init__()

        #save system updates
        UpdateScene('YesOrNo')

        self.scene2_bg = pygame.image.load('day1/day1_anime/mcronalds.png').convert_alpha() 
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
        self.choice1 = self.choice_font.render('Sure', True, self.white)

        #square surrounding choice1
        self.choice1_rect = pygame.Rect(0, 0, 500, 32)
        self.choice1_rect.centerx = self.text_bar_rect.centerx
        self.choice1_rect.centery = self.text_bar_rect.centery - 40
        self.choice1_rect2 = self.choice1.get_rect(center = self.choice1_rect.center)

        #choice2
        self.choice2 = self.choice_font.render('Sorry— kinda wanted to eat alone.', True, self.white)

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
                        previous_scene = 'YesOrNo'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()
                    
                    #choice1
                    if self.choice1_rect.collidepoint(mouse):
                        Yes(self.screen)
                        running = False

                    #choice2
                    if self.choice2_rect.collidepoint(mouse):
                         No(self.screen)
                         running = False

            pygame.display.flip()


class No(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

         #save system updates
        UpdateScene('No')
        UpdatePoints('Mary', -3)

        self.scene3_bg = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.scene3_bg = pygame.transform.smoothscale(self.scene3_bg, (self.screen_width, self.screen_height))

        self.new_bg = pygame.image.load('day1/day1_anime/mcronalds.png').convert_alpha()
        self.new_bg = pygame.transform.smoothscale(self.new_bg, (self.screen_width, self.screen_height))

        self.mary = pygame.image.load('day1/day1_anime/mary.png').convert_alpha()

        original_rect = self.mary.get_rect()
        desired_width = 1500
        aspect_ratio = original_rect.height / original_rect.width
        desired_height = int(desired_width * aspect_ratio)

        self.mary = pygame.transform.smoothscale(self.mary, (desired_width, desired_height))
        self.show_mary = True

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4, self.text5]

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(The woman pauses for a moment, the edge of her smile faltering just slightly.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text2(self):
        text = "???: Oh. Got it. No problem."

        #save system updates
        UpdateTextIdx(self.text_idx)
        
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (255, 182, 193))
        self.text_idx += 1
        self.add_to_back_log(text, color = (255, 182, 193))
    
    def text3(self):
        text = "(She nods, polite but a little distant, then walks off, disappearing into the lunchtime crowd. You claim the table alone, unpack your tray, and begin to eat.)"

        #save system updates
        UpdateTextIdx(self.text_idx)
        
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.show_mary = False
    
    def text4(self):
        text = "(Around you, people talk, laugh, shift trays. You chew in silence, every bite echoing a little too loud in your head.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text5(self):
        text = "(The drive home is uneventful—just the blur of roads and stoplights. When you finally unlock your door and drop your bag by the side of your bed, the exhaustion hits you all at once.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def run(self):
        running = True

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        while running:
            self.screen.blit(self.new_bg, (0,0 ))
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            if self.text_idx >= 5:
                if not self.fade_started:
                    self.fading = True
                    self.fade_alpha = 0
                    self.fade_started = True

                if self.fading:
                    if self.fade_alpha < 255:
                        self.screen.blit(self.new_bg, (0, 0))

                        fading_bg = self.scene3_bg.convert()
                        fading_bg.set_alpha(self.fade_alpha)

                        self.screen.blit(fading_bg, (0,0))
                        self.fade_alpha += 15
                        self.fade_alpha = min(self.fade_alpha, 255)
                    else:
                        self.fade_alpha = 255
                        self.fading = False

                elif not self.fading: 
                    self.screen.blit(self.scene3_bg, (0, 0))
            
            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:

                if self.show_mary:
                    mary_rect = self.mary.get_rect()
                    mary_rect.midbottom= ((self.screen_width // 2) - 150, self.screen_height)
                    self.screen.blit(self.mary, mary_rect)

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
                        previous_scene = 'No'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)

            self.clock.tick(60)
            pygame.display.flip()

class Yes(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('Yes')
        UpdatePoints('Mary', 3)

        self.scene3_bg = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.scene3_bg = pygame.transform.smoothscale(self.scene3_bg, (self.screen_width, self.screen_height))

        self.new_bg = pygame.image.load('day1/day1_anime/mcronalds.png').convert_alpha()
        self.new_bg = pygame.transform.smoothscale(self.new_bg, (self.screen_width, self.screen_height))

        self.mary = pygame.image.load('day1/day1_anime/mary.png').convert_alpha()

        original_rect = self.mary.get_rect()
        desired_width = 1500
        aspect_ratio = original_rect.height / original_rect.width
        desired_height = int(desired_width * aspect_ratio)

        self.mary = pygame.transform.smoothscale(self.mary, (desired_width, desired_height))
        self.show_mary = True

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4]

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(The woman smiles immediately—but there's something too fast about it. Like she knew your answer before you even gave it.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text2(self):
        text = "???: Thanks. It's impossible to find a table in this crowd."
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (255, 182, 193))
        self.text_idx += 1
        self.add_to_back_log(text, color = (255, 182, 193))
    
    def text3(self):
        text = "(You nod, distracted by the way she neatly unwraps her sandwich, fingers moving in slow, deliberate motions.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text4(self):
        text = "(The two of you eat in silence. The noise of McRonalds buzzes around like static, too distant to feel real. The silence feels uncomfortable.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def run(self):
        running = True

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        while running:
            self.screen.blit(self.new_bg, (0,0 ))
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time
            
            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:

                if self.show_mary:
                    mary_rect = self.mary.get_rect()
                    mary_rect.midbottom= ((self.screen_width // 2) - 150, self.screen_height)
                    self.screen.blit(self.mary, mary_rect)

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
                        StartMaryConvo(self.screen)
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
                        previous_scene = 'Yes'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)
                    
            self.clock.tick(60)
            pygame.display.flip()
            
