import pygame as pg
import sys


class Game:
    def __init__(self):
        pg.init()

        windowSize = (700,500)
        self.window = pg.display.set_mode(windowSize)

        self.FPS = 60

        self.clock = pg.time.Clock()
        pg.display.set_caption("PyUndertale")

    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    

            self.window.fill("black")

            pg.display.update()
            self.clock.tick(self.FPS)
                    


if __name__ == '__main__':
    game = Game()
    game.run()