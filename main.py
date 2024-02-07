import pygame as pg
import sys
from sceneCache import SceneCache
from settings import GameData


class Game:
    def __init__(self):
        pg.init()

        windowSize = (700,500)
        self.window = pg.display.set_mode(windowSize)

        self.FPS = 60

        self.clock = pg.time.Clock()
        pg.display.set_caption("PyUndertale")

        self.gameData = {
            GameData.CurrentEnemy : None
        }

        self.sceneCache = SceneCache(self)
        self.currentScene = self.sceneCache.overWorld()
        
        self.fpsFont = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)


    def displayFPS(self):
        fontColor = (255,255,255)
        fps = self.fpsFont.render(f"{round(self.clock.get_fps())}",True,fontColor)
        pos = (670,10)
        self.window.blit(fps,pos)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                
                
            self.window.fill("black")

            self.currentScene.update()

            self.sceneCache.battle().buttonPressedTimer.update()
            self.displayFPS()
            pg.display.update()
            self.clock.tick(self.FPS)
                    


if __name__ == '__main__':
    game = Game()
    game.run()
