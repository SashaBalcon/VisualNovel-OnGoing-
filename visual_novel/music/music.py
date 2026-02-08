import pygame
import os

def init_music():
    pygame.mixer.init()

def play_music(filename, loop = True, volume = 0.5, fade = 3000):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)

    pygame.mixer.music.load(full_path)

    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0, fade_ms = fade)

def stop_music(fade = 2000):
    pygame.mixer.music.fadeout(fade)
