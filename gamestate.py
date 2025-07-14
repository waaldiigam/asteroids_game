import pygame

class GameState(pygame.sprite.Sprite):

    containers = ()

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = 0
        self.lives = 0
        self.font = pygame.font.SysFont(None, 30)
        
    def draw(self, screen):        
        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (50, 100))