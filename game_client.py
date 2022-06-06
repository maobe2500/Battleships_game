import pygame
import sys
from square import Square
from network import Network

class Game:
    def __init__(self):
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.BLUE = (44, 132, 232)
        self.RED = (250, 134, 123)
        self.BLOCK_SIZE = 20
        self.WIDTH = 400
        self.HEIGHT = 400
        self.CHAT_AREA = 200

        self.SCREEN = pygame.display.set_mode((self.WIDTH + self.CHAT_AREA, self.HEIGHT))
        self.SCREEN.fill(self.BLUE)
        self.ships_left = 10
        self.sea = {}
        self.network = Network(self.SCREEN)

        self.init_grid()

    def event_check(self):
        self.network.loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.check_click(event.pos)

    def init_grid(self):
        for i in range(0, self.WIDTH, self.BLOCK_SIZE):  
            for j in range(0, self.HEIGHT, self.BLOCK_SIZE): 
                pos = (i + self.BLOCK_SIZE//2, j + self.BLOCK_SIZE//2)
                s = Square(pos, self.BLOCK_SIZE)
                self.sea[pos] = s

    def draw_grid(self):
        for square in self.sea.values():
            if square.pos in self.network.enemy_hits:
                square.set_color(self.RED)
            square.draw(self.SCREEN)
        pygame.display.update()

    def check_click(self, event_pos):
        for square in self.sea.values():
            if square.is_pressed(event_pos):
                print(f"square at {square.pos} is clicked, new color: {square.color}")
                if self.ships_left > 0:
                    square.set_color(self.BLACK)
                    self.network.ship_locations[square] = {"hits": 0, "max_hits":1}
                    self.ships_left -= 1
                else:
                    square.set_color(self.BLUE)
                    self.network.hits.append(square.pos)

 
    def main_loop(self):
        while True:
            self.event_check()
            self.draw_grid()
    

def main():
    g = Game()
    g.main_loop()

if __name__ == "__main__":
    main()