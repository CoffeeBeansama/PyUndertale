import pygame as pg
from enum import Enum
from scene import Scene
from player import PlayerSoul
from support import loadSprite
from eventHandler import EventHandler

class Turn(Enum):
    PlayerTurn = 1
    EnemyTurn = 2

class Battle(Scene):
    
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)

        self.visibleSprites = pg.sprite.Group()
        
        self.player = PlayerSoul((100,100),self.visibleSprites,self.collisionSprites)
        self.eventHandler = EventHandler()

        self.createButtons()

        self.currentTurn = Turn.PlayerTurn
        self.turns = {
            Turn.PlayerTurn : self.playerTurn,
            Turn.EnemyTurn : self.enemyTurn
        }

    def createButtons(self):
        spritePath = "Sprites/UI/"
        buttonSize = (50,30)
        self.buttonSprites = {
            "Fight" : loadSprite(f"{spritePath}FightButton.png",buttonSize),
            "Act" : loadSprite(f"{spritePath}ActButton.png",buttonSize),
            "Item" : loadSprite(f"{spritePath}ItemButton.png",buttonSize),
            "Mercy" : loadSprite(f"{spritePath}MercyButton.png",buttonSize)
        }

    def playerTurn(self):
        pass

    def enemyTurn(self):
        for sprites in self.visibleSprites:
            self.screen.blit(sprites.sprite,sprites.rect.center)
    
    def handleInput(self):
        self.eventHandler.handlePlayerInput()

        if self.eventHandler.pressingRightButton():
            pass
        if self.eventHandler.pressingLeftButton():
            pass

    def update(self):  
        self.handleInput()
      
        getCurrentTurn = self.turns.get(self.currentTurn)
        getCurrentTurn()
        
        self.player.update()
