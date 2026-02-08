import pygame
import sys
import os
from .c1c1 import C1C1
from .c1c2 import C1C2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx
from template import Template
from save_system.save_ui import SaveUI
from game_state import game_state
from print_text import SlowText

'''
If you select choice 1 (Stay at home), it immediatley goes to this
'''

class C1(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('C1')
        UpdateDay1Flags('main_choice', 'stay home')

        self.scene2_bg = pygame.image.load('day1/day1_anime/frame57.png').convert_alpha()
        self.scene2_bg = pygame.transform.smoothscale(self.scene2_bg, (self.screen_width, self.screen_height))

        self.scene3_bg = pygame.image.load('day1/day1_anime/frame1_32.png').convert_alpha()
        self.scene3_bg = pygame.transform.smoothscale(self.scene3_bg, (self.screen_width, self.screen_height))

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3]

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(Socially interacting when you're this tired feels like a chore, and going out to work sounds even worse. Ultimately, it's an easy choice to call out of work. It's an even easier choice to fall back into your fluffy bedsheets and fall asleep.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

        #save system updates
        UpdateTextIdx(self.text_idx)

    def text2(self):
        text = "(You groan awake. It's already evening, but you still feel no less awake than you did in the morning. Even so, you force yourself awake enough to trade out your pajamas for regular clothes and grab your computer from where it's been charging.  You open your computer, slowly flicking through shows... Thursday, Breaking Drugs, My Little Horse, Two Piece- oh! You'd heard that show was interesting; you could try it out now.)"
        
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

        #save system updates
        UpdateTextIdx(self.text_idx)
    
    def text3(self):
        text = "(Two hours later, you decide that you need to eat. However, when you go into your kitchen scavenging for food, you find chips and... well, just chips. Great, just what you needed.)"
        
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

        #save system updates
        UpdateTextIdx(self.text_idx)

    def run(self):
        running = True
        played_animation = False

        text_run = True
        text_pressed = False
        log_show = False

        while running:
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            #if the animation has played switch the background
            if played_animation:
                self.screen.blit(self.scene3_bg, (0,0 ))
            else: 
                self.screen.blit(self.scene2_bg, (0, 0))
            
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
                    if self.text_idx == 1:
                        C1S2(self.screen)
                        played_animation = True
                    if self.text_idx < len(self.text_funcs):
                        self.text_funcs[self.text_idx]() 
                        text_run = True
                    elif self.text_idx < len(self.text_funcs) + 1:
                        self.text_idx = self.text_idx + 1
                    else:
                        C1_1(self.screen)
                    text_pressed = False

                if log_show:
                    pygame.draw.rect(self.screen, self.button_color, self.popup)
                    pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                    self.screen.blit(self.x, self.x_text_rect)
                    
                    self.back_log_hist()

                #popup
            if self.popup_visible:
                pygame.draw.rect(self.screen, self.button_color, self.popup)
                pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                self.screen.blit(self.x, self.x_text_rect)

                #exit button
                pygame.draw.rect(self.screen, self.button_color2, self.button_rect2)
                self.screen.blit(self.quit_button2, self.text_rect_button2)

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
                        previous_scene = 'C1'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)


            self.clock.tick(60)
            pygame.display.flip()

class C1S2(Template):
    def __init__(self, screen):
        self.screen = screen
        super().__init__()

        self.width, self.height = self.screen.get_size()

        self.fps = 8
        self.num_frames = 32
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "day1_anime/")
        self.font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fonts", "SendFlowers-Regular.ttf")

        self.frames = self.load_frames(self.path, self.num_frames)
        self.run()

    def load_frames(self, path, num_frames):
        frames = []
        for i in range(num_frames):
            filename = os.path.join(path, f"frame1_{i}.png")
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.smoothscale(image, (self.width, self.height))
            frames.append(image)
        return frames

    def run(self):
        frame_idx = 0
        clock = pygame.time.Clock()
        running = True

        while running:
            mouse = pygame.mouse.get_pos()

            # animation frames
            self.screen.blit(self.frames[frame_idx], (0, 0))

            # exit button
            #pygame.draw.rect(self.screen, self.button_color, self.exit_rect)
            #self.screen.blit(self.exit, self.text_exit_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

            pygame.display.flip()
            frame_idx = (frame_idx + 1) % self.num_frames
            clock.tick(self.fps)

            if frame_idx == self.num_frames - 1:
                running = False

class C1_1(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen
        super().__init__()

        #save system updates
        UpdateScene('C1_1')

        self.scene2_bg = pygame.image.load('day1/day1_anime/frame1_32.png').convert_alpha()
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
        self.choice1 = self.choice_font.render('Eat out at McDonalds', True, self.white)

        #square surrounding choice1
        self.choice1_rect = pygame.Rect(0, 0, 500, 32)
        self.choice1_rect.centerx = self.text_bar_rect.centerx
        self.choice1_rect.centery = self.text_bar_rect.centery - 40
        self.choice1_rect2 = self.choice1.get_rect(center = self.choice1_rect.center)

        #choice2
        self.choice2 = self.choice_font.render('Get groceries to cook at home', True, self.white)

        #square surrounding choice2
        self.choice2_rect = pygame.Rect(0, 0, 500, 32)
        self.choice2_rect.centerx = self.text_bar_rect.centerx
        self.choice2_rect.centery = self.text_bar_rect.centery
        self.choice2_rect2 = self.choice2.get_rect(center = self.choice2_rect.center)

    def Choice(self):
        pass

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
                        previous_scene = 'C1_1'
                        save_screen = SaveUI(self.screen, previous_scene, 1)
                        save_screen.run()
                    
                    
                    #choice1
                    if self.choice1_rect.collidepoint(mouse):
                        C1C2(self.screen)
                        running = False

                    #choice2
                    if self.choice2_rect.collidepoint(mouse):
                         C1C1(self.screen)
                         running = False

            pygame.display.flip()