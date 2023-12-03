import pygame as pg
from support import loadSprite
from timer import Timer
from eventHandler import EventHandler

class PlayerAttack:
     def __init__(self):
         self.screen = pg.display.get_surface()
         self.crossHair = loadSprite("Sprites/Player/playerCrossHair.png",(100,100))
         self.crossHairRect = self.crossHair.get_rect(topleft=(300,70))
         
         self.attackColor = (255,255,255)
         self.attackStartRadius = 300
         self.currentAttackRadius = self.attackStartRadius
         self.attackPosition = [352,119]
         self.attackThickness = 3

         self.attackSpeed = 3.5
         self.targetRadius = 45
         self.timer = Timer(200)
         self.eventHandler = EventHandler()

         self.playerShotted = False
         

     def handlePlayerInput(self):
         self.timer.update()
         self.eventHandler.handlePlayerInput()
         
         if self.eventHandler.pressingInteractButton():
            if not self.timer.activated:
               if self.currentAttackRadius <= self.targetRadius:
                  if self.currentAttackRadius >= 3:
                     print("Perfect Shot!")
                  else:
                     print("Missed!")
                  self.playerShotted = True
               self.timer.activate()

     def update(self):
         self.handlePlayerInput()
         
         if not self.playerShotted:
            if self.currentAttackRadius > 1:
               self.currentAttackRadius -= self.attackSpeed
         
         pg.draw.circle(self.screen,self.attackColor,
	                 self.attackPosition,
	                 self.currentAttackRadius,
	                 self.attackThickness)
         
         self.targetCrossHair = self.screen.blit(self.crossHair,self.crossHairRect)
