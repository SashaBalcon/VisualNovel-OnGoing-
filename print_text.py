import sys
import os
import pygame

'''
This is the class to print the text
'''

class SlowText:
    def __init__(self, text=None, pos=(0, 0), line_length=600, italicized=False, colored=(255, 255, 255)):
        self.text = text
        self.rendered_text = ""
        self.characters = list(text)
        self.clock = pygame.time.Clock()
        self.delay = 30  # ms per letter
        self.line_length = line_length
        self.pos = pos

        # Font
        self.font_path = "Fonts/ArchitectsDaughter-Regular.ttf"
        self.text_font = pygame.font.Font(self.font_path, 23)

        self.color = colored
        self.start_time = pygame.time.get_ticks()
        self.idx = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.idx < len(self.characters) and current_time - self.start_time > self.delay:
            self.rendered_text += self.characters[self.idx]
            self.idx += 1
            self.start_time = current_time

    def UpdateFast(self):
        self.Clear()
        self.idx = len(self.characters)
        self.rendered_text = "".join(self.characters)

    def Clear(self):
        self.rendered_text = ""
        self.idx = 0

    def Draw(self, screen):
        new_x, new_y = self.pos
        line = ""
        words = self.rendered_text.split(" ")
        word_count = len(words)
        i = 0

        while i < word_count:
            if i < word_count - 1:
                next_chunk = words[i] + " "
            else:
                next_chunk = words[i]

            chunk_width, chunk_height = self.text_font.size(line + next_chunk)

            if chunk_width > self.line_length:
                text_surface = self.text_font.render(line, True, self.color)
                screen.blit(text_surface, (new_x, new_y))
                new_y += chunk_height + 5
                line = next_chunk
            else:
                line += next_chunk

            i += 1

        if line:
            text_surface = self.text_font.render(line, True, self.color)
            screen.blit(text_surface, (new_x, new_y))


'''
Sources:
https://www.pygame.org/docs/ref/font.html

'''