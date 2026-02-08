import pygame
import sys
import os
from style import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from begin_scene.content_warning import ContentTitle

'''
This is the next tkinker window that gives you options on how to start the game
'''

screen, SCREEN_WIDTH, SCREEN_HEIGHT  = SetUp()
header_font, smaller_font = GetFont()

class StartingOptions:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Load background image (make sure path is correct)
        self.bg_image = pygame.image.load("main_menu/images/paper_background.png").convert_alpha()

        # Button properties
        self.button_color = (154, 159, 142)  # #9A9F8E
        self.text_color = (0, 0, 0)
        self.buttons = []

        # Button rects (centered on screen)
        button_width, button_height = 300, 60
        start_y = self.height // 2 - 100
        gap = 80

        # Button labels and their callbacks
        button_data = [
            ("New Game", self.start_new_game),
            ("Settings", self.settings),
            ("Load Save", self.load_save),
            ("Back", self.back),
        ]

        for i, (text, callback) in enumerate(button_data):
            rect = pygame.Rect(
                (self.width // 2 - button_width // 2, start_y + i * gap),
                (button_width, button_height)
            )
            self.buttons.append({"rect": rect, "text": text, "callback": callback})

        self.running = True

    def draw(self):
        bg_rect = self.bg_image.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.bg_image, bg_rect.topleft)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            rect = button["rect"]
            text = button["text"]
            # Highlight if hovered
            color = (120, 125, 110) if rect.collidepoint(mouse_pos) else self.button_color

            pygame.draw.rect(self.screen, color, rect)
            # Draw text centered
            text_surf = header_font.render(text, True, self.text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["callback"]()

    def start_new_game(self):
        # Close this screen and original start screen (if needed)
        self.running = False
        ContentTitle()

    def settings(self):
        # Placeholder: call your settings screen here
        open_settings(self.screen)  # Adapt if this needs a different parameter

    def load_save(self):
        print("Load save - not implemented yet")

    def back(self):
        self.running = False
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()
            clock.tick(60)
