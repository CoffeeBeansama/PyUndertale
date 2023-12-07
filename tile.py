import pygame as pg
from support import loadSprite
from settings import tileSize


class WallTile(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)

        self.sprite = image
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)
        self.mask = pg.mask.from_surface(self.sprite)











