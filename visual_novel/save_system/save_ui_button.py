import pygame
import os
from save_system.save_data import save_data_dict

class SaveButtons:
    def __init__(self, screen):
        self.screen = screen
        self.option = 1
        self.screen_width, self.screen_height = self.screen.get_size()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(BASE_DIR, '..', 'Fonts', 'SendFlowers-Regular.ttf')
        self.font_path2 = os.path.join(BASE_DIR, '..', 'Fonts', 'ArchitectsDaughter-Regular.ttf')

        self.button_font = pygame.font.Font(self.font_path, 30)
        self.ok_font = pygame.font.Font(self.font_path, 40)
        self.text_font = pygame.font.Font(self.font_path2, 25)

        self.white = (255, 255, 255)
        self.button_color = (88, 117, 113)
        self.black = (0, 0, 0)

        self.panel_color = (62, 95, 102)

        self.save()
        self.load()
        self.back()
        self.arrows()

    def save(self):
        self.save_button = self.button_font.render('Save', True, self.white)

        self.save_rect = pygame.Rect(0, 0, 90, 50)

        center_x = (self.screen_width // 2) - 100
        center_y = self.screen_height - 25
    
        self.save_rect.center = (center_x, center_y)
        self.text_save_rect = self.save_button.get_rect(center = self.save_rect.center)

    def load(self):
        self.load_button = self.button_font.render('Load', True, self.white)

        self.load_rect = pygame.Rect(0, 0, 90, 50)

        center_x = (self.screen_width // 2) + 100
        center_y = self.screen_height - 25
    
        self.load_rect.center = (center_x, center_y)
        self.text_load_rect = self.load_button.get_rect(center = self.load_rect.center)

    def arrows(self):
        self.arrow_left = self.text_font.render('<', True, self.white)
        self.arrow_right = self.text_font.render('>', True, self.white)

        self.right_rect = pygame.Rect(0, 0, 40, 35)
        self.left_rect = pygame.Rect(0, 0, 40, 35)

        center_x_right = (self.screen_width // 2) + 25
        center_y_right = self.screen_height - 75

        center_x_left = (self.screen_width // 2) - 25
        center_y_left = self.screen_height - 75

        self.right_rect.center = (center_x_right, center_y_right)
        self.left_rect.center = (center_x_left, center_y_left)

        self.text_right_arrow = self.arrow_right.get_rect(center = self.right_rect.center)
        self.text_left_arrow = self.arrow_left.get_rect(center = self.left_rect.center)

    def back(self):
        self.back_button = self.button_font.render('Back', True, self.white)

        self.back_rect = pygame.Rect(0, 0, 90, 50)

        center_x = (self.screen_width // 2)
        center_y = self.screen_height - 25
    
        self.back_rect.center = (center_x, center_y)
        self.text_back_rect = self.back_button.get_rect(center = self.back_rect.center)

    def RectMessages(self, option):
        """
        This makes the buttons to check if you want to save, load, or overwrite a save file...
        """
        #making the main message

        match option:
            case 1:
                self.message  = self.text_font.render('Please press Load or Save first.', True, self.white)
            case 2:
                self.message = self.text_font.render('Overwrite save file?', True, self.white)

        self.rect_message = pygame.Rect(0, 0, 450, 200)
        self.rect_message.center = (self.screen_width // 2, self.screen_height // 2)
        self.message_surface_rect = self.message.get_rect(center = self.rect_message.center)
        
        #making the ok button
        self.ok_surface = self.text_font.render('OK', True, self.white)

        self.ok_rect = pygame.Rect(0, 0, 50, 50)
        self.ok_rect.midbottom = (self.rect_message.centerx, self.rect_message.bottom - 10)

        self.ok_surface_rect = self.ok_surface.get_rect(center = self.ok_rect.center)

        self.no = self.text_font.render('NO', True, self.white)
        self.yes = self.text_font.render('YES', True, self.white)

        self.no_rect = pygame.Rect(0, 0, 70, 50)
        self.yes_rect = pygame.Rect(0, 0, 70, 50)

        self.no_rect.midbottom = (self.rect_message.right - 100, self.rect_message.bottom - 10)
        self.yes_rect.midbottom = (self.rect_message.left + 100, self.rect_message.bottom - 10)

        self.no_surface_rect = self.no.get_rect(center = self.no_rect.center)
        self.yes_surface_rect = self.yes.get_rect(center = self.yes_rect.center)

    def renderButtons(self):
        #save button
        pygame.draw.rect(self.screen, self.button_color, self.save_rect)
        self.screen.blit(self.save_button, self.text_save_rect)

        #load button
        pygame.draw.rect(self.screen, self.button_color, self.load_rect)
        self.screen.blit(self.load_button, self.text_load_rect)

        #back button
        pygame.draw.rect(self.screen, self.button_color, self.back_rect)
        self.screen.blit(self.back_button, self.text_back_rect)

