import pygame as pg
from support import import_folder,loadSprite
from random import random
from abc import ABC,abstractmethod

class Player(ABC,pg.sprite.Sprite):
    def __init__(self, pos,groups,collisionSprites):
        super().__init__(groups)
        self.collisionSprites = collisionSprites
        
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
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.handleVerticalMovement(-1,"Up")
        elif keys[pg.K_DOWN]:
            self.handleVerticalMovement(1,"Down")
        elif keys[pg.K_LEFT]:
            self.handleHorizontalMovement(-1,"Left")
        elif keys[pg.K_RIGHT]:
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
    def __init__(self, pos, groups, collisionSprites, spawnAreas, enterBattleScene):
        super().__init__(pos, groups, collisionSprites)
        self.spawnAreas = spawnAreas
        self.enterBattleScene = enterBattleScene

        self.sprite = pg.image.load(f"{self.spritePath}Down/0.png").convert_alpha()
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.state = "Down_idle"

        self.frame_index = 0
        self.walkingAnimationTime = 1 / 8
        
        self.importSprites()

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

    def handleSpawnAreaCollision(self):
        for spawnTile in self.spawnAreas:
            if spawnTile.hitbox.colliderect(self.hitbox) and not spawnTile.playerCollided:
                spawnProbability = random()
                spawnChance = 0.1
                if spawnProbability < spawnChance:
                    self.enterBattleScene()
                spawnTile.playerCollided = True 
            elif not spawnTile.hitbox.colliderect(self.hitbox) and spawnTile.playerCollided:
                spawnTile.playerCollided = False

    def update(self):
        self.handleInputs()
        self.handleAnimation()
        self.handleSpawnAreaCollision()
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