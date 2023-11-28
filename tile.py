import pygame as pg
from support import loadSprite
from settings import tileSize


class WallTile(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.sprite = loadSprite("Sprites/wall.png",(tileSize,tileSize))
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

class SpawnArea(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.sprite = loadSprite("Sprites/player.png",(tileSize,tileSize))
        self.sprite.set_alpha(50)
        self.playerCollided = False
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)











