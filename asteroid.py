from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_NEW_SPEED
import random
import pygame

class Asteroid(CircleShape):

    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen, dt):
        pygame.draw.circle(screen, (255, 255, 255), (self.position), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        r_angle = random.uniform(20.0, 50.0)
        new_vector1 = self.velocity.rotate(r_angle)
        new_vector2 = self.velocity.rotate(-r_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = new_vector1 * ASTEROID_NEW_SPEED
        new_asteroid2.velocity = new_vector2 * ASTEROID_NEW_SPEED