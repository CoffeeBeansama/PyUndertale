import pygame as pg
from timer import Timer
from support import loadSprite


class BoneObject:
  def __init__(self,pos):
      self.screen = pg.display.get_surface()
      self.spritePath = "Sprites/Bone.png"
      self.sprite = loadSprite(self.spritePath,(18,10)).convert_alpha()
      self.rect = self.sprite.get_rect(topleft=pos)
      
      self.damage = 1
      self.obj = None
      
  def renderedObject(self):
      self.obj = self.screen.blit(self.sprite,self.rect)

    
  
