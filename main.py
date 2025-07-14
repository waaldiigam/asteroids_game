# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gamestate import GameState

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    shoots = pygame.sprite.Group()

    Shot.containers = (shoots, drawable, updatable)
    
    AsteroidField()   

    GameState.containers = (drawable)
    game_state =  GameState()

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return        
        screen.fill((0, 0, 0))
        for thing in drawable:
            thing.draw(screen)
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.detect_collision(player):
                print("Game over!")
                return
            for bullet in shoots:
                if bullet.detect_collision(asteroid):
                    game_state.score += 1
                    asteroid.split()
                    bullet.kill()
        dt = clock.tick(60) / 1000
        pygame.display.flip()     
        
        
if __name__ == "__main__":
    main()
