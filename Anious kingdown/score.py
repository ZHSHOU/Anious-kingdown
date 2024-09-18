import pygame

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
    
    def add_score(self):
        self.score += 10  # 每次匹配加10分
    
    def display(self, screen, width):
        score_text = f"Score: {self.score}"
        text_surface = self.font.render(score_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(width - 150, 10))  # 设置在右上角
        screen.blit(text_surface, text_rect)


