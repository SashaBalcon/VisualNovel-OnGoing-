import pygame
import sys
import tkinter as tk
import game_state 
from print_text import SlowText
import os

'''
This is the parent class that all of the routes draw from
'''

class Template:
    def __init__(self, screen = None):
        game_state.width, game_state.height = game_state.screen.get_size()
        self.screen_width, self.screen_height = game_state.width, game_state.height
        self.font_path = "Fonts/SendFlowers-Regular.ttf"

        self.font_text = "Fonts/ArchitectsDaughter-Regular.ttf"
        self.text_font = pygame.font.Font(self.font_text, 15)

        self.button_font = pygame.font.Font(self.font_path, 23)

        self.white = (255, 255, 255)
        self.button_color = (88, 117, 113)
        self.button_color2 = (62, 95, 102)
        self.back_log_history = []
        next_scene = None

        self.fading = False
        self.fade = None

        self.scroll_offset = 0
        self.max_scroll = 0

        #for fading in scenes
        self.faded = False

        self.save()
        self.options()
        self.back_log()
        self.options_popup()
        self.exit_button()
        self.setup_save_button()
        self.setup_exit_button()
        self.inven()
        self.text_bar()

    def save(self):
        self.save_button = self.button_font.render('Save', True, self.white)

        self.save_rect = pygame.Rect(0, 0, 70, 50)
        self.save_rect.center = (1200, 900)
        self.text_save_rect = self.save_button.get_rect(center = self.save_rect.center)
    
    def options(self):
        self.options_button = self.button_font.render('Options', True, self.white)

        self.option_rect = pygame.Rect(0, 0, 75, 50)
        self.option_rect.center = (1292, 900)
        self.options_button_rect = self.options_button.get_rect(center=self.option_rect.center)

    def back_log(self):
        self.back_log = self.button_font.render('Log', True, self.white)

        self.log_rect = pygame.Rect(0, 0, 75, 50)
        self.log_rect.center = (100, 900)
        self.log_button_rect = self.back_log.get_rect(center = self.log_rect.center)

    def options_popup(self):

        #popup rectangle
        self.popup = pygame.Rect(0, 0, 500, 450)
        self.popup.center = (self.screen_width // 2, self.screen_height // 2)

        #x button
        self.x = self.button_font.render('X', True, self.white)

        #square surrounding x button
        self.mini_x = pygame.Rect(self.popup.left + 10, self.popup.top + 10, 20, 20)
        self.x_text_rect = self.x.get_rect(center=self.mini_x.center)

        self.popup_visible = False

    def setup_save_button(self):
        self.save_button_surface2 = self.button_font.render('Save', True, self.white)

        self.save_rect2 = pygame.Rect(0, 0, 70, 50)
    
        self.save_rect2.centerx = self.popup.centerx + 45
        self.save_rect2.top = self.popup.top + 50

        self.text_save_rect2 = self.save_button_surface2.get_rect(center=self.save_rect2.center)

    def exit_button(self):
        self.quit_button = self.button_font.render('Quit', True, self.white)

        self.button_rect = pygame.Rect(0, 0, 70, 50)
        self.button_rect.centerx = self.popup.centerx
        self.button_rect.top = self.popup.top + 50
        self.text_rect_button = self.quit_button.get_rect(center = self.button_rect.center)

    def setup_exit_button(self):
        self.quit_button2 = self.button_font.render('Quit', True, self.white)

        self.button_rect2 = pygame.Rect(0, 0, 70, 50)
        self.button_rect2.centerx = self.popup.centerx - 45
        self.button_rect2.top = self.popup.top + 50
        self.text_rect_button2 = self.quit_button2.get_rect(center = self.button_rect2.center)

    def inven(self):
        self.inven_button = self.button_font.render('Inventory',True, self.white)

        self.inven_rect = pygame.Rect(0, 0, 100, 50)
        self.inven_rect.center = (1400, 900)
        self.text_inven_rect = self.inven_button.get_rect(center = self.inven_rect.center)

    def text_bar(self):
        self.bg = pygame.Surface((self.screen_width, 300), pygame.SRCALPHA).convert_alpha()
        self.bg.fill((0, 0, 0, 150)) 

        self.text_bar_rect = self.bg.get_rect()
        self.text_bar_rect.midbottom = (self.screen_width // 2, self.screen_height)

    def add_to_back_log(self, new_line, color= None):
        if color is None:
            color = self.white
        self.back_log_history.append((new_line, color))

    def get_wrapped_text_height(self, text, max_width):
        words = text.split()
        space_width, space_height = self.text_font.size(' ')
        line_width = 0
        lines = 1

        for word in words:
            word_width, _ = self.text_font.size(word)
            if line_width + word_width <= max_width:
                line_width += word_width + space_width
            else:
                lines += 1
                line_width = word_width + space_width
        return lines * (space_height + 5)

    def back_log_hist(self):
        y = 50
        max_width = self.popup.width - 40
        x = self.popup.left + 20

        total_height = 0
        i = 1
    
        for line, color in self.back_log_history[-15:]:
            prefix = f"line {i}: "
            full_line = prefix + line
            total_height += self.get_wrapped_text_height(full_line, max_width)
            i += 1

        visible_height = self.popup.height - 70
        self.max_scroll = max(0, total_height - visible_height)
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

        old_clip = self.screen.get_clip()
        self.screen.set_clip(self.popup)

        y = 50 - self.scroll_offset
        i = 1

        for line, color in self.back_log_history[-15:]:
            prefix = f"line {i}: "
            full_line = prefix + line
            self.render_wrapped_text(full_line, x, self.popup.top + y, max_width, color)
            y += self.get_wrapped_text_height(full_line, max_width)
            i += 1

        self.screen.set_clip(old_clip)


    def render_wrapped_text(self, text, x, y, max_width, color):
        words = text.split()
        space_width, space_height = self.text_font.size(' ')
        line = ""
        line_width = 0

        for word in words:
            word_width, _ = self.text_font.size(word)
            if line_width + word_width <= max_width:
                line += word + " "
                line_width += word_width + space_width
            else:
                rendered = self.text_font.render(line.strip(), True, color)
                self.screen.blit(rendered, (x, y))
                y += space_height + 5
                line = word + " "
                line_width = word_width + space_width

        if line:
            rendered = self.text_font.render(line.strip(), True, color)
            self.screen.blit(rendered, (x, y))

    def collide_instructions(self, event, mouse):

        #quit button instructions
        if self.button_rect.collidepoint(mouse):
            pygame.quit()
            sys.exit()
            
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

    def draw_buttons(self):
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

    def display_text(self, text, color=None):

        self.slow_text = SlowText(
            text,
            pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10),
            line_length=self.text_bar_rect.width - 40,
            colored=color
        )
        self.text_idx += 1
        self.add_to_back_log(text, color=color)

    def CharacterSprites(self, character):
        match character:
            case 'Sammy':
                sammy_path = os.path.join( "sprites", "sammy")
                sammy_expressions = {
                    "neutral_work": pygame.image.load(os.path.join(sammy_path, "neutral_work_sammy.png")).convert_alpha(),
                    "angry_work": pygame.image.load(os.path.join(sammy_path, "angry_work_sammy.png")).convert_alpha(),
                    "happy_work": pygame.image.load(os.path.join(sammy_path, "happy_work_sammy.png")).convert_alpha(),
                    "excited_work": pygame.image.load(os.path.join(sammy_path, "excited_work_sammy.png")).convert_alpha(),
                    "embarrassed_work": pygame.image.load(os.path.join(sammy_path, "embarrassed_work_sammy.png")).convert_alpha()
                }

                desired_width = 850

                for key in sammy_expressions:
                    img = sammy_expressions[key]
                    original_width, original_height = img.get_size()
                    aspect_ratio = original_height / original_width
                    desired_height = int(desired_width * aspect_ratio)
                    sammy_expressions[key] = pygame.transform.smoothscale(img, (desired_width, desired_height))
                
                return sammy_expressions




            


'''
Sources: 
https://medium.com/@01one/how-to-work-with-fullscreen-in-pygame-893ec4eb25ae
https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
https://stackoverflow.com/questions/42577197/pygame-how-to-correctly-use-get-rect
https://www.pygame.org/docs/ref/rect.html
https://docs.python.org/3/library/threading.html
'''