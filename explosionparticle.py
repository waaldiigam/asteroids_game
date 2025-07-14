import random
import pygame
from circleshape import CircleShape

class ExplosionParticle(CircleShape):

    containers = ()

    def __init__(self, x, y, angle, life_time):
        super().__init__(x, y, random.randint(1, 5))
        self.angle = angle
        self.speed = random.uniform(50, 300)
        self.velocity = pygame.Vector2(1, 0).rotate(self.angle) * self.speed
        self.life_time = life_time
        self.age = 0

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt
        if self.age > self.life_time:
            self.kill()

    def draw(self, screen, dt):
        pygame.draw.circle(screen, (201, 201, 201), self.position, self.radius)        