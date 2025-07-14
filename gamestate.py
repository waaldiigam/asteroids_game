from constants import LIFE_RADIUS, LIFE_MAX_NUM, SCREEN_WIDTH, SCREEN_HEIGHT
from gamestatus import GameStatus
import pygame

class GameState(pygame.sprite.Sprite):

    containers = ()

    def __init__(self, dt):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = 0
        self.lifes = LIFE_MAX_NUM
        self.font = pygame.font.SysFont(None, 30)
        self.life_position = [(85, 55), (105, 55), (125, 55)]
        self.game_status = GameStatus.START
        self.timer = 0
        self.font_small = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 150)
        self.pause_font = pygame.font.SysFont(None, 50)
        self.show_press_space = True
        self.game_hidden_score = 0

    def triangle(self, position):
        forward = pygame.Vector2(0, 1).rotate(180)
        right = pygame.Vector2(0, 1).rotate(90) * LIFE_RADIUS / 1.5
        a = position + forward * LIFE_RADIUS
        b = position - forward * LIFE_RADIUS - right
        c = position - forward * LIFE_RADIUS + right
        return [a, b, c]

    def draw_life(self, screen):
        missing_life = 3 - self.lifes
        for i in range(0, LIFE_MAX_NUM):
            if i >= missing_life:
                pygame.draw.polygon(screen, (255, 255, 255), self.triangle(self.life_position[len(self.life_position)-i-1]), 1)
            else:
                pygame.draw.polygon(screen, (105, 105, 105), self.triangle(self.life_position[len(self.life_position)-i-1]), 1)

    def draw(self, screen, dt):  
        if self.game_status != GameStatus.GAME_OVER:        
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 15))

            lifes_text = self.font.render("Lives: ", True, (255, 255, 255))
            screen.blit(lifes_text, (10, 50))

            self.draw_life(screen)
        
        if self.game_status == GameStatus.START:            
            title = self.title_font.render("Asteroids - but bad!", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(title, title_rect)

            self.timer += dt
            if self.timer >= 0.5:
                self.show_press_space = not self.show_press_space
                self.timer = 0

            if self.show_press_space:
                prompt = self.font_small.render("Press ENTER to start", True, (255, 255, 255))
                prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))                
                screen.blit(prompt, prompt_rect)
        
        if self.game_status == GameStatus.PAUSED:
            pause = self.pause_font.render(f"Press ENTER to continue, current lifes: {self.lifes}", True, (255, 255, 255))
            prompt_rect = pause.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
            screen.blit(pause, prompt_rect)

        if self.game_status is GameStatus.GAME_OVER:
            game_over = self.title_font.render(f"GAME OVER!!!!", True, (255, 255, 255))
            title_rect = game_over.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over, title_rect)

            score = self.font_small.render(f"You were able to gain {self.score} score", True, (255, 255, 255))
            prompt_rect = score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))                
            screen.blit(score, prompt_rect)

            self.timer += dt
            if self.timer >= 0.5:
                self.show_press_space = not self.show_press_space
                self.timer = 0

            if self.show_press_space:
                prompt = self.font_small.render("Press ENTER to restart", True, (255, 255, 255))
                prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1))                
                screen.blit(prompt, prompt_rect)
        

