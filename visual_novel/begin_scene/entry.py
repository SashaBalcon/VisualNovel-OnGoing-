import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from music.music import init_music, play_music, stop_music

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scene1 import Scene1

class Entry:
    def __init__(self, screen):

        stop_music()
        init_music()

        play_music("music_assets/insane.mp3", loop=True, volume = 0.3)
        
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.fps = 10
        self.num_frames = 100
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images_beg/")
        self.font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fonts", "SendFlowers-Regular.ttf")

        self.frames = self.load_frames(self.path, self.num_frames)
        self.run()

    def load_frames(self, path, num_frames):
        frames = []
        for i in range(1, num_frames + 1):
            filename = os.path.join(path, "entry_title-" + str(i) + ".png")
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

        journal_loader = JournalEntries(self.screen)
        loaded_journals = journal_loader.load()
        for key in ["journal_one-", "journal_two-", "journal_three-"]:
            JournalPlayer(self.screen, loaded_journals[key])
        next_scene = Scene1(self.screen)
        next_scene.run()


class JournalEntries:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.entry_frames = {
            "journal_one-" : 196,
            "journal_two-" : 228,
            "journal_three-" : 228
        }

        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images_beg/")

        self.loaded_frames = {}
    
    def load(self):
        for entry_name, num_frames in self.entry_frames.items():
            frames = []
            for i in range(1, num_frames + 1):
                filename = os.path.join(self.path, entry_name + str(i) + ".png")
                image = pygame.image.load(filename).convert_alpha()
                image = pygame.transform.smoothscale(image, (self.width, self.height))
                frames.append(image)
            self.loaded_frames[entry_name] = frames
        return self.loaded_frames

class JournalPlayer:
    def __init__(self, screen, frames):
        self.frames = frames
        self.num_frames = len(self.frames)

        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.fps = 18
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        frame_idx = 1
        running = True

        while running:

            self.screen.blit(self.frames[frame_idx], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

            pygame.display.flip()
            frame_idx = (frame_idx + 1) % self.num_frames
            clock.tick(self.fps)

            if frame_idx == self.num_frames - 1:
                running = False

        


        