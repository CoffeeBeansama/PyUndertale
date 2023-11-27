import pygame as pg
from scene import Scene
from camera import CameraGroup
from player import Player

class OverWorld(Scene):
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)

        self.visibleSprites = CameraGroup()

        self.collisionSprites = pg.sprite.Group()

        self.player = Player((100,100),self.visibleSprites,self.collisionSprites)

    
    def update(self):
        self.player.update()
        self.visibleSprites.custom_draw(self.player)
        

