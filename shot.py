from circleshape import CircleShape
from constants import SHOT_RADIUS
import pygame


class Shot(CircleShape):
    
    containers = ()

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen, dt):
        pygame.draw.circle(screen, (255, 255, 255), (self.position), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt