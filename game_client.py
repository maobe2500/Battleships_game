import pygame
from square import Square
from network import Network

class Game:
    def __init__(self):
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.BLUE = (44, 132, 232)
        self.WINDOW_HEIGHT = 900
        self.WINDOW_WIDTH = 900
        self.BLOCK_SIZE = int(self.WINDOW_HEIGHT/30)

        self.SCREEN = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(self.BLUE)
        self.sea = {}

        self.network = Network()

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.check_click(event.pos)


    def drawGrid(self):
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                pos = (x + self.BLOCK_SIZE/2, y + self.BLOCK_SIZE/2)
                s = Square(pos, "./Resources/sea_small.png", self.BLOCK_SIZE)
                s.draw(self.SCREEN)
                #rect = pygame.Rect(x, y, blockSize, blockSize)
                #pygame.draw.rect(self.SCREEN, self.WHITE, rect, 1)
                self.sea[pos] = s
        pygame.display.update()

    def check_click(self, event_pos):
        for square in self.sea.values():
            if square.is_pressed(event_pos):
                square.set_color((250,25,25), self.SCREEN)
                self.network.send(f"{event_pos}")
                pygame.display.update()
                

    def is_a_hit(self):
        pass

    def shoot(self):
        pass

    def main_loop(self):
        while True:
            self.event_check()
            self.drawGrid()

def main():
    g = Game()
    g.main_loop()

if __name__ == "__main__":
    main()