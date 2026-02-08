import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template import Template
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx, UpdatePoints
from save_system.save_ui import SaveUI
from game_state import game_state
from fade_out import FadeOut
from print_text import SlowText

class SlugLiar(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen
        super().__init__()

        #save system updates
        UpdateScene('SlugLiar')

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
        self.choice1 = self.choice_font.render('What got you so into sea slugs anyway?', True, self.white)

        #square surrounding choice1
        self.choice1_rect = pygame.Rect(0, 0, 500, 32)
        self.choice1_rect.centerx = self.text_bar_rect.centerx
        self.choice1_rect.centery = self.text_bar_rect.centery - 40
        self.choice1_rect2 = self.choice1.get_rect(center = self.choice1_rect.center)

        #choice2
        self.choice2 = self.choice_font.render(" Oh… uh… yeah… They're cool (Lying)", True, self.white)

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
                        previous_scene = 'SlugLiar'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()
                    
                    #choice1
                    if self.choice1_rect.collidepoint(mouse):
                        yay_slugs(self.screen)
                        running = False

                    #choice2
                    if self.choice2_rect.collidepoint(mouse):
                         ew_slugs(self.screen)
                         running = False

            pygame.display.flip()

class yay_slugs(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()
        #save system updates
        UpdateScene('yay_slugs')
        UpdatePoints('Sammy', 2)

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
        text = "Sammy: Huh? What do you mean?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))
    
    def text2(self):
        text = "You: Well, they're not exactly…"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text3(self):
        text = " Sammy: Appealing? Interesting? Hehe, yeah, I guess they do seem that way. But check this out. These things are Nudibranchs, and they’re classified as hermaphrodites."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text4(self):
        text = "You: …Ok?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text5(self):
        text = "Sammy: They have both male and female reproductive organs. Isn't that cool?"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text6(self):
        text = "You: Actually yeah, kinda. "

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text7(self):
        text = "Sammy: You may not see it as I do, but this is the most interesting thing in the world to me, and I- oh shit! I still need to finish my work! Uh- I'll catch you later."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.sammy_show = True
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text8(self):
        text = "(Sammy runs off in the direction from which you came, making you realize that you also still have work to do. You finish your tasks to the best of your ability, clock out, and head home.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.sammy_show = False


    def run(self):
        running = True
        played_animation = False

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        self.screen.blit(self.aquirium, (0, 0))

        if self.text_idx >= 6:
                self.screen.blit(self.bg2, (0, 0))

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            self.screen.blit(self.aquirium, (0, 0))

            if self.text_idx <= 7:
                    self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
                    self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47
                    self.screen.blit(self.sammy["excited_work"], (self.pos_x, self.pos_y))
    
            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:
        
                #text bar
                self.screen.blit(self.bg, self.text_bar_rect)

                #inventory button
                pygame.draw.rect(self.screen, self.button_color, self.inven_rect)
                self.screen.blit(self.inven_button, self.text_inven_rect)

                #save button
                pygame.draw.rect(self.screen, self.button_color, self.save_rect)
                self.screen.blit(self.save_button, self.text_save_rect)

                #options button
                pygame.draw.rect(self.screen, self.button_color, self.option_rect)
                self.screen.blit(self.options_button, self.options_button_rect)

                #backlog button
                pygame.draw.rect(self.screen, self.button_color, self.log_rect)
                self.screen.blit(self.back_log, self.log_button_rect)
                
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

                    #quit button instructions
                    if self.button_rect.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

                    #save button instructions
                    if self.save_rect2.collidepoint(mouse):
                        previous_scene = 'yay_slugs'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #options instructions
                    if self.option_rect.collidepoint(mouse) and not self.popup_visible:
                        self.popup_visible = True
                    
                    if self.mini_x.collidepoint(mouse):
                        self.popup_visible = False
                    
                    if self.inven_rect.collidepoint(mouse):
                        self.popup_visible = False

                    #log instructions
                    if self.log_rect.collidepoint(mouse) and not log_show:
                        log_show = True
                    
                    if self.mini_x.collidepoint(mouse):
                        log_show = False

                    if event.button == 4:  # scroll up
                        self.scroll_offset = max(0, self.scroll_offset - 20)
                    elif event.button == 5:  # scroll down
                        self.scroll_offset = min(self.max_scroll, self.scroll_offset + 20)


            self.clock.tick(60)
            pygame.display.flip()

class ew_slugs(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()
        #save system updates
        UpdateScene('ew_slugs')
        UpdatePoints('Sammy', 2)

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
        text = "(Sammy furrows her brow and shoots daggers at you through her gaze. A slight redness appears in her cheeks, though she never breaks her eye contact with you.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text2(self):
        text = "Sammy: If you're gonna lie to me, you may as well not say anything at all."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text3(self):
        text = "You: No I-"
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text4(self):
        text = "Sammy: Oh, cut the bullshit already, I'd much rather you have given it to me straight."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text5(self):
        text = "(Sammy glances over at the tank once again and looks away immediately, almost too embarrassed to look.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text6(self):
        text = "Sammy: Fucking shit, you dragged me away from my work for this too."

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (173, 113, 217))
        self.text_idx += 1
        self.add_to_back_log(text,  color = (173, 113, 217))

    def text7(self):
        text = "(Before you can say anything else, Sammy storms off and rushes in the direction from which you came.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.sammy_show = False

    def text8(self):
        text = "(You're all too stunned when you realize that you still have work you have yet to finish. You get about half of it done, expecting a hefty lecture from your supervisor next shift, but it's over regardless. You clock out and head home for the day.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.sammy_show = False


    def run(self):
        running = True
        played_animation = False

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            if self.text_idx > 7:
                self.screen.blit(self.bg2,(0,0))
            else:
                self.screen.blit(self.aquirium, (0, 0))

            if self.text_idx <= 4:
                self.pos_x = (self.screen_width // 2) - (self.sammy["neutral_work"].get_width() // 2)
                self.pos_y = self.screen_height - self.sammy["neutral_work"].get_height() - 47
                self.screen.blit(self.sammy["angry_work"], (self.pos_x, self.pos_y))
            elif self.text_idx >= 5 and self.text_idx < 8:
                self.screen.blit(self.sammy["embarrassed_work"], (self.pos_x, self.pos_y))

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
                
                if self.text_idx > 7:
                    if not self.faded:
                            self.fade = FadeOut('day1/day1_anime/aquirium.png', 'day1/day1_anime/night.png', self.screen)
                            self.faded = True
                            self.fade.run()

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
                        previous_scene = 'ew_slugs'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)


            self.clock.tick(60)
            pygame.display.flip()
