from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def detect_collision(self, circleShapeObject):
        if self.radius + circleShapeObject.radius > pygame.Vector2.distance_to(self.position, circleShapeObject.position):
            return True
        return False