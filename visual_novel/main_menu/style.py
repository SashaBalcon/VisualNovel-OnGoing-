import os
import pygame

'''
Main menu template
'''

pygame.init()

#font path
base_dir = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(base_dir, "..", "Fonts", "SendFlowers-Regular.ttf")
FONT = os.path.normpath(FONT)

#Image paths
MAIN_BG = "main_menu/images/start_screen.png" 
TITLE_BG = "main_menu/images/image-2.png"
TITLE = "main_menu/images/title.png"
PAPER_POPUP = "main_menu/images/paper_background.png"

# Colors
BUTTON_BG_COLOR = (154, 159, 142)
BUTTON_HOVER_COLOR = (120, 125, 110)
BUTTON_TEXT_COLOR = (0, 0, 0)
POPUP_BG_COLOR = (245, 245, 220)

def GetFont():
    header_font = pygame.font.Font(FONT, 50)
    smaller_font = pygame.font.Font(FONT, 30)
    return header_font, smaller_font

def LoadedImage(path):
    img = pygame.image.load(path).convert_alpha()
    return img

def SetUp():
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Bleed")
    return screen, SCREEN_WIDTH, SCREEN_HEIGHT 