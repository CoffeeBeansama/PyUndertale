import pygame as pg
from support import import_folder,loadSprite
from timer import Timer
from abc import ABC,abstractmethod
from eventHandler import EventHandler

class Player(ABC,pg.sprite.Sprite):
    def __init__(self, pos,groups,collisionSprites):
        super().__init__(groups)
        self.collisionSprites = collisionSprites
        
        self.eventHandler = EventHandler()

        self.maxHP = 20
        self.currentHP = self.maxHP

        self.speed = 2
        self.spritePath = "Sprites/Player/"
        self.direction = pg.math.Vector2()

    
    def handleMovement(self):
        self.hitbox.x += self.direction.x * self.speed
        self.handleWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.handleWallCollision("Vertical")
        self.rect.center = self.hitbox.center

    def handleVerticalMovement(self,value,state):
        self.direction.x = 0
        self.direction.y = value
        self.state = state

    def handleHorizontalMovement(self,value,state):
        self.direction.x = value
        self.direction.y = 0
        self.state = state

    def handleWallCollision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "Horizontal":
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left
                elif direction == "Vertical":
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top
    
    def handleInputs(self):
        self.eventHandler.handlePlayerInput()
  
        if self.eventHandler.pressingUpButton():
            self.handleVerticalMovement(-1,"Up")

        elif self.eventHandler.pressingDownButton():
            self.handleVerticalMovement(1,"Down")

        elif self.eventHandler.pressingLeftButton():
            self.handleHorizontalMovement(-1,"Left")

        elif self.eventHandler.pressingRightButton():
            self.handleHorizontalMovement(1,"Right")
            
        else:
            self.idleState()

    def idleState(self):
        self.direction.x = 0
        self.direction.y = 0
        if not "_idle" in self.state:
            self.state = f"{self.state}_idle"
    
    @abstractmethod
    def update(self):
        pass

class Frisk(Player):
    def __init__(self, pos, groups, collisionSprites, npcs, enterBattleScene):
        super().__init__(pos, groups, collisionSprites)
        self.npcSprites = npcs
        self.enterBattleScene = enterBattleScene

        self.sprite = pg.image.load(f"{self.spritePath}Down/0.png").convert_alpha()
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.state = "Down_idle"

        self.frame_index = 0
        self.walkingAnimationTime = 1 / 8
        
        self.importSprites()

        self.timer = Timer(200)

    def importSprites(self):
        self.animationStates = {
            "Up": [], "Down": [], "Left": [], "Right" : [],
            "Down_idle": [],"Up_idle": [], "Left_idle": [] , "Right_idle": [],
            
        }

        for animations in self.animationStates.keys():
            fullPath = self.spritePath + animations
            self.animationStates[animations] = import_folder(fullPath)

    def handleAnimation(self):
        animation = self.animationStates[self.state]
        self.frame_index += self.walkingAnimationTime 

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.sprite = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.sprite.get_rect(center=self.hitbox.center)

    def handleNPCInteraction(self):
        for npc in self.npcSprites:
            if npc.hitbox.colliderect(self.hitbox):
                if not self.timer.activated:
                    if self.eventHandler.pressingInteractButton():
                        npc.interact()
                    self.timer.activate()
            else:
                npc.disengage()

    def update(self):
        self.timer.update()
        self.handleInputs()
        self.handleAnimation()
        self.handleNPCInteraction()
        self.handleMovement()

class PlayerSoul(Player):
    def __init__(self, pos, groups, collisionSprites):
        super().__init__(pos, groups, collisionSprites)

        self.sprite = loadSprite(f"{self.spritePath}PlayerSoul.png",(24,24))
        startingPos = (338,220)
        self.rect = self.sprite.get_rect(topleft=startingPos)
        self.hitbox = self.rect.inflate(0,0)

    def update(self):
        self.handleInputs()
        self.handleMovement()