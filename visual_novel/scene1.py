import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from day1.scene1_1 import Scene1_1

'''
This plays a simple animation to open the game
'''

class Scene1:
    def __init__(self, screen):
        pygame.init()

        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.fps = 8
        self.num_frames = 57
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "day1/day1_anime/")
        self.font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fonts", "SendFlowers-Regular.ttf")

        self.frames = self.load_frames(self.path, self.num_frames)
        self.run()

    def load_frames(self, path, num_frames):
        frames = []
        for i in range(1, num_frames):
            filename = os.path.join(path, "frame" + str(i) + ".png")
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

            pygame.display.flip()
            frame_idx = (frame_idx + 1) % self.num_frames
            clock.tick(self.fps)

            if frame_idx == self.num_frames - 1:
                running = False

        # Run Scene2 after Scene1 finishes
        next_scene = Scene1_1(self.screen)
        next_scene.run()

'''
Sources:
https://www.geeksforgeeks.org/python-display-images-with-pygame/
https://www.geeksforgeeks.org/pygame-character-animation/
https://pypi.org/project/moviepy/
https://zulko.github.io/moviepy/getting_started/index.html#getting-started
'''