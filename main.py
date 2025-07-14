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
from gamestatus import GameStatus
from explosionparticle import ExplosionParticle

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("img/background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    GameState.containers = (drawable)
    game_state =  GameState(dt)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, game_state)

    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    shoots = pygame.sprite.Group()

    Shot.containers = (shoots, drawable, updatable)
    
    a_field = AsteroidField()

    explosions = pygame.sprite.Group()
    ExplosionParticle.containers = (explosions, updatable, drawable)

    def kill_all(objects):
        for object in objects:
            object.kill()
    

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_state.game_status is GameStatus.START:
                print("Game Start!")
                kill_all(asteroids)
                game_state.game_status = GameStatus.PLAYING                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_state.game_status is GameStatus.PAUSED:
                print("Restart")
                game_state.game_status = GameStatus.PLAYING
                kill_all(asteroids)
                player.velocity = pygame.Vector2(0, 0)
                player.weapon_upgrade = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_state.game_status is GameStatus.GAME_OVER:
                print("Game over")
                kill_all(asteroids)                
                game_state.lifes = 3
                game_state.score = 0
                game_state.game_hidden_score = 0
                player.velocity = pygame.Vector2(0, 0)
                player.weapon_upgrade = 0
                game_state.game_status = GameStatus.PLAYING
        screen.blit(background, (0, 0))
        for thing in drawable:
            thing.draw(screen, dt)
        if game_state.game_status in [GameStatus.START, GameStatus.PAUSED]:
            asteroids.update(dt)           
            a_field.update(dt)
        if game_state.game_status is GameStatus.PLAYING:
            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.detect_collision(player):
                    player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2) 
                    game_state.lifes -= 1
                    game_state.game_hidden_score = 0
                    game_state.game_status = GameStatus.PAUSED
                    kill_all(asteroids)
                    kill_all(shoots)
                    kill_all(explosions)                     
                for bullet in shoots:
                    if bullet.detect_collision(asteroid):
                        game_state.score += 1
                        game_state.game_hidden_score += 1
                        asteroid.split()
                        bullet.kill()
        if game_state.game_hidden_score == 100:
            game_state.game_hidden_score = 0
            if game_state.lifes < 3:
                game_state.lifes += 1
            elif player.weapon_upgrade < PLAYER_WEAPON_MAX_UPGRADE:
                player.weapon_upgrade += 1
        if game_state.lifes == 0:
            print("Game Over!")
            game_state.game_status = GameStatus.GAME_OVER            
        dt = clock.tick(60) / 1000
        pygame.display.flip()     
        
        
if __name__ == "__main__":
    main()
