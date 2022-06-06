import pygame

class Square():
    def __init__(self, pos, block_size):
        pygame.init()
        self.pos = pos
        self.size = (block_size, block_size)
        self.color = (255,255,0)
        self.rect = pygame.Rect(self.pos, (block_size, block_size))

    def draw(self, screen):
        self.rect.centerx, self.rect.centery = self.pos
        pygame.draw.rect(screen, self.color, self.rect)
    
    def is_pressed(self, event_pos):
        return self.rect.collidepoint(event_pos)

    def set_color(self, color):
        self.color = color