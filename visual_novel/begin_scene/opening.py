import pygame
import sys
import os

from .entry import Entry

class Opening:
    def __init__(self, screen):
        
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.fps = 7
        self.num_frames = 55
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images_beg/")
        self.font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fonts", "SendFlowers-Regular.ttf")

        self.frames = self.load_frames(self.path, self.num_frames)
        self.run()

    def load_frames(self, path, num_frames):
        frames = []
        for i in range(1, num_frames + 1):
            filename = os.path.join(path, "opening" + str(i) + ".png")
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.smoothscale(image, (self.width, self.height))
            frames.append(image)
        return frames

    def run(self):
        frame_idx = 1
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

            pygame.display.flip()
            frame_idx = (frame_idx + 1) % self.num_frames
            clock.tick(self.fps)

            if frame_idx == self.num_frames - 1:
                running = False

        next_scene = Entry(self.screen)
        next_scene.run()

