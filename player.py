from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_BOOST_DRAIN_RATE, PLAYER_MAX_BOOST, PLAYER_BOOST_RECHARGE_RATE, SCREEN_HEIGHT, SCREEN_WIDTH
from shot import Shot
from gamestatus import GameStatus
from gamestate import GameState
from explosionparticle import ExplosionParticle
import random
import pygame

class Player(CircleShape):
    
    containers = ()
    
    def __init__(self, x, y, game_state):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.game_state = game_state
        self.velocity = pygame.Vector2(0, 0)
        self.boost_energy = PLAYER_MAX_BOOST
        self.max_boost_energy = PLAYER_MAX_BOOST
        self.boost_drain_rate = PLAYER_BOOST_DRAIN_RATE
        self.boost_recharge_rate = PLAYER_BOOST_RECHARGE_RATE
        self.weapon_upgrade = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        
    def draw(self, screen, dt):
        if self.game_state.game_status == GameStatus.PLAYING:
            pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
            bar_width = 200
            bar_height = 10
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = (SCREEN_HEIGHT) - 30
            fill_ratio = self.boost_energy / self.max_boost_energy
            fill_width = int(bar_width * fill_ratio)
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, fill_width, bar_height))
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                if self.weapon_upgrade == 0:
                        self.timer = PLAYER_SHOOT_COOLDOWN                
                        self.shoot()
                if self.weapon_upgrade == 1:
                        self.timer = PLAYER_SHOOT_COOLDOWN /1.3
                        self.shoot()
                if self.weapon_upgrade == 2:                    
                        self.timer = PLAYER_SHOOT_COOLDOWN                
                        self.double_shoot()
                if self.weapon_upgrade == 3:
                        self.timer = PLAYER_SHOOT_COOLDOWN /1.3
                        self.double_shoot()

        self.position += self.velocity * dt
        self.velocity *- 0.95
        self.timer -= dt

        boosting = keys[pygame.K_LSHIFT] and self.boost_energy > 0
        if boosting:
            self.boost(dt)
        else:
            self.boost_energy += self.boost_recharge_rate * dt
            if self.boost_energy > self.max_boost_energy:
                self.boost_energy = self.max_boost_energy
        
        super().update(dt)


    def move(self, dt):        
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt
        self.spawn_enginge_particles(2)            

    def boost(self, dt):
        self.boost_energy -= self.boost_drain_rate * dt
        if self.boost_energy < 0:
            self.boost_energy = 0
            return
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * 2 * PLAYER_SPEED * dt
        self.spawn_enginge_particles(10)
        
    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def double_shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation)
        offset = 8
        left_gun_position = self.position - right * offset
        right_gun_position = self.position + right * offset
        bullet_left = Shot(left_gun_position.x, left_gun_position.y)
        bullet_right = Shot(right_gun_position.x, right_gun_position.y)
        bullet_velocity = forward * PLAYER_SHOOT_SPEED
        bullet_left.velocity = bullet_velocity
        bullet_right.velocity = bullet_velocity

    def spawn_enginge_particles(self, num_particles):
        back_offset = pygame.Vector2(0, 1).rotate(self.rotation + 180)
        spawn_pos = self.position + back_offset * self.radius
        for _ in range(num_particles):
            jitter = random.uniform(-15, 15)
            ExplosionParticle(spawn_pos.x, spawn_pos.y, self.rotation - 90 + jitter , 0.2)