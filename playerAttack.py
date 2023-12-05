import pygame as pg
from support import loadSprite
from timer import Timer
from eventHandler import EventHandler

class PlayerAttack():
     def __init__(self,damageEnemy):
         
         self.damageEnemy = damageEnemy
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

         self.startAttack = False
         self.currentAttackActive = 0
         self.attackActive = [False,False,False]
         
     
     def startPlayerAttack(self):
         if not self.timer.activated:
            self.startAttack = True
            self.timer.activate()

     def hitTheSweetSpot(self):
         if self.currentAttackRadius <= self.targetRadius:
            if self.currentAttackRadius >= 3:
               return True
            else: return False
     

     def handlePlayerInput(self):
         self.eventHandler.handlePlayerInput()
         
         if self.eventHandler.pressingInteractButton():
            if not self.timer.activated:
               if self.hitTheSweetSpot():
                  self.damageEnemy()
            self.timer.activate()
        
     def createAttack(self,pos,ID,speed):
         self.handlePlayerInput()
             
         if self.currentAttackRadius > 1:
            self.currentAttackRadius -= speed
         
         pg.draw.circle(self.screen,self.attackColor,
	                 pos,
	                 self.currentAttackRadius,
	                 self.attackThickness)
         
         self.targetCrossHair = self.screen.blit(self.crossHair,(pos[0]-52,pos[1]-49))         


     def update(self):
         self.timer.update()
         
         for i in range(len(self.attackActive)):
            self.createAttack([100+(240*i),119],i,0.5)
         
