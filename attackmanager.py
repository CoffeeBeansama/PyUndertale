import pygame as pg
from timer import Timer
from attackobj import BoneObject
from support import loadSprite

class PapyrusAttack:
  def __init__(self):
      self.screen = pg.display.get_surface()

      self.spawnTimer = Timer(600)

      self.projectiles = []

      self.attacks = {
        1: self.attackOne,
        2: self.attackTwo
      }
  

  def attackOne(self):
      self.spawnTimer.update()
      if not self.spawnTimer.activated:
         newAttack = BoneObject((0,150))
         self.projectiles.append(newAttack)
         newAttack.sprite = loadSprite(newAttack.spritePath,(18,(10 + (len(self.projectiles) * 15 )))).convert_alpha()         

         self.spawnTimer.activate()


      for bone in self.projectiles:
          bone.rect.x += 3
          bone.renderedObject()

  def attackTwo(self):
      self.spawnTimer.update()
      if not self.spawnTimer.activated:
         newAttack = BoneObject((700,150))
         self.projectiles.append(newAttack)
         newAttack.sprite = loadSprite(newAttack.spritePath,(18,(10 + (len(self.projectiles) * 15 )))).convert_alpha()         

         self.spawnTimer.activate()

      for bone in self.projectiles:
          bone.rect.x -= 3
          bone.renderedObject()

