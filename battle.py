import pygame as pg
from scene import Scene
from player import PlayerSoul

class Battle(Scene):
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)

        self.visibleSprites = pg.sprite.Group()
        
        self.player = PlayerSoul((100,100),self.visibleSprites,self.collisionSprites)

    
    def update(self):
        for sprites in self.visibleSprites:
            self.screen.blit(sprites.sprite,sprites.rect.center)

        
        self.player.update()
