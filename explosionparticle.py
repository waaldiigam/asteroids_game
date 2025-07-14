import random
import pygame
from circleshape import CircleShape
from constants import PARTICLE_LIFETIME

class ExplosionParticle(CircleShape):

    containers = ()

    def __init__(self, x, y):
        super().__init__(x, y, random.randint(1, 5))
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(50, 300)
        self.velocity = pygame.Vector2(1, 0).rotate(self.angle) * self.speed
        self.lifetime = PARTICLE_LIFETIME
        self.age = 0

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt
        if self.age > self.lifetime:
            self.kill()

    def draw(self, screen, dt):
        pygame.draw.circle(screen, (201, 201, 201), self.position, self.radius)        