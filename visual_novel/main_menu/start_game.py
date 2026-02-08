import pygame
import sys
import os

from style import *
from start_options import StartingOptions

pygame.init()  

screen, SCREEN_WIDTH, SCREEN_HEIGHT  = SetUp()
header_font, smaller_font = GetFont()

class Button:
    def __init__(self, rect, text, font, command, hovering=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.command = command
        self.hovering = hovering

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovering else BUTTON_BG_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        txt_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.command()

class StartScreen:
    def __init__(self):
        self.running = True
        self.show_quit_popup = False

        self.bg_image = LoadedImage(MAIN_BG)
        self.title_bg_img = LoadedImage(TITLE_BG)
        self.title_img = LoadedImage(TITLE)

        # Scale title background and center it
        self.title_bg_img = pygame.transform.smoothscale(self.title_bg_img, (self.title_bg_img.get_width(), self.title_bg_img.get_height()))
        self.title_bg_rect = self.title_bg_img.get_rect(center=(SCREEN_WIDTH // 2, 300))

        # Scale and center title image on top
        self.title_rect = self.title_img.get_rect(center=(SCREEN_WIDTH // 2, 300))

        # Buttons setup
        btn_width, btn_height = 300, 70
        btn_x = SCREEN_WIDTH // 2 - btn_width // 2
        btn_y_start = int(SCREEN_HEIGHT * 0.6)

        self.start_button = Button((btn_x, btn_y_start, btn_width, btn_height), "Start Game", header_font, self.start_game)
        self.quit_button = Button((btn_x, btn_y_start + btn_height + 20, btn_width, btn_height), "Quit Game", header_font, self.show_quit_popup_func)

        # Popup buttons (initialized later)
        self.popup_buttons = []

    def show_quit_popup_func(self):
        self.show_quit_popup = True

    def draw_quit_popup(self):
        popup_width, popup_height = 500, 500
        popup_rect = pygame.Rect((SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2), (popup_width, popup_height))

        # Background
        pygame.draw.rect(screen, POPUP_BG_COLOR, popup_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), popup_rect, 3, border_radius=10)

        # Background image inside popup
        paper_img = LoadedImage(PAPER_POPUP)
        paper_img = pygame.transform.smoothscale(paper_img, (popup_width, popup_height))
        screen.blit(paper_img, popup_rect)

        # Quit Text
        text_surf = smaller_font.render("Are you sure you'd like to quit the game?", True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, popup_rect.top + 60))
        screen.blit(text_surf, text_rect)

        # Popup buttons
        if not self.popup_buttons:
            btn_w, btn_h = 150, 75
            left_btn = Button((popup_rect.left + 80, popup_rect.top + 150, btn_w, btn_h), "Quit", smaller_font, self.quit_confirm)
            right_btn = Button((popup_rect.right - 80 - btn_w, popup_rect.top + 150, btn_w, btn_h), "Nevermind", smaller_font, self.quit_cancel)
            self.popup_buttons = [left_btn, right_btn]

        for btn in self.popup_buttons:
            btn.draw(screen)

    def quit_confirm(self):
        pygame.quit()
        sys.exit()

    def quit_cancel(self):
        self.show_quit_popup = False
        self.popup_buttons = []  # Clear popup buttons to reset next time

    def start_game(self):
        starting_options = StartingOptions(screen)
        starting_options.run()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.show_quit_popup:
                            self.show_quit_popup = False
                        else:
                            self.running = False

                # Handle events for buttons
                self.start_button.handle_event(event)
                self.quit_button.handle_event(event)

                if self.show_quit_popup:
                    for btn in self.popup_buttons:
                        btn.handle_event(event)

            # Draw everything
            screen.blit(self.bg_image, (0, 0))
            screen.blit(self.title_bg_img, self.title_bg_rect)
            screen.blit(self.title_img, self.title_rect)

            if self.show_quit_popup:
                self.draw_quit_popup()
            else:
                self.start_button.draw(screen)
                self.quit_button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    StartScreen().run()
