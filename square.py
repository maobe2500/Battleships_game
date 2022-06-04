import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self, pos, path, block_size):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.image.load(path).convert_alpha()
        #self.tint_image_overlay = pygame.Surface(self.image.get_size()).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        self.rect.centerx, self.rect.centery = self.pos
        screen.blit(self.image, self.rect)
    
    def is_pressed(self, event_pos):
        return self.rect.collidepoint(event_pos)

    def change_color(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)
        
        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage

    def set_color(self, color, screen):
        color_image = self.change_color(self.image, color)
        self.image = color_image
        screen.blit(color_image, color_image.get_rect(center=self.pos))