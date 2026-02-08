import pygame

class FadeOut:
    def __init__(self, bg1, bg2, screen, duration = 700):
        self.screen = screen
        self.duration = duration
        self.start_time = pygame.time.get_ticks()

        self.bg1 = pygame.image.load(bg1).convert()
        self.bg2 = pygame.image.load(bg2).convert()
        self.bg1 = pygame.transform.scale(self.bg1, self.screen.get_size())
        self.bg2 = pygame.transform.scale(self.bg2, self.screen.get_size())

    def run(self):
        clock = pygame.time.Clock()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                        
            now = pygame.time.get_ticks()
            elapsed = now - self.start_time
            progress = min(1, elapsed / self.duration)

            # Blend the two backgrounds
            blended = self.bg1.copy()
            self.bg2.set_alpha(int(progress * 255))
            blended.blit(self.bg2, (0, 0))

            self.screen.blit(blended, (0, 0))
            pygame.display.flip()

            if progress >= 1:
                done = True

            clock.tick(60)

