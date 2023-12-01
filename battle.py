import pygame as pg
from enum import Enum
from scene import Scene
from timer import Timer
from settings import GameData
from player import PlayerSoul
from support import loadSprite
from eventHandler import EventHandler

class Turn(Enum):
    PlayerTurn = 1
    EnemyTurn = 2

class ButtonData(Enum):
     Sprite = 1
     SpriteSelected = 2
     Position = 3
     Event = 4

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

        self.selectionIndex = 0
        self.buttonPressedTimer = Timer(150)

        self.spritePath = "Sprites/Player/"
        self.playerSelectionSprite = loadSprite(f"{self.spritePath}PlayerSoul.png",(20,20))
        startingPos = (52,425)
        self.playerSelectionRect = self.playerSelectionSprite.get_rect(topleft=startingPos)

        self.currentEnemy = None

    def createButtons(self):
        spritePath = "Sprites/UI/"
        buttonSize = (140,70)

        self.playerButton = {
            "Fight": { ButtonData.Event : self.fightButton },
            "Act": { ButtonData.Event : self.actButton },
            "Item": { ButtonData.Event : self.itemButton },
            "Mercy": { ButtonData.Event : self.mercyButton }
        }

        for i,key in enumerate(self.playerButton.keys()):
             self.playerButton[key][ButtonData.Sprite] = loadSprite(f"{spritePath}{key}Button.png",buttonSize)
             self.playerButton[key][ButtonData.SpriteSelected] = loadSprite(f"{spritePath}{key}ButtonSelected.png",buttonSize)
             self.playerButton[key][ButtonData.Position] = (40+(160*i),400)

        self.buttons = [i for i in self.playerButton.values()]
        
    def uponEnterScene(self):
        self.currentEnemy = self.game.gameData[GameData.CurrentEnemy]
        print(self.currentEnemy)

    def handleInput(self):
        self.eventHandler.handlePlayerInput()
        self.buttonPressedTimer.update()

        if not self.buttonPressedTimer.activated:

            if self.eventHandler.pressingRightButton():
                self.selectionIndex += 1
            if self.eventHandler.pressingLeftButton():
                self.selectionIndex -= 1
                
            if self.eventHandler.pressingInteractButton():
                self.buttons[self.selectionIndex][ButtonData.Event]()
    
            self.buttonPressedTimer.activate()

        if self.selectionIndex < 0:
             self.selectionIndex = 0

        if self.selectionIndex > len(self.buttons) -1:
             self.selectionIndex = int(len(self.buttons)) - 1
    

    def fightButton(self):
        print("fight")
    
    def actButton(self):
        print("act")

    def itemButton(self):
        print("item")

    def mercyButton(self):
        print("mercy")


    def playerTurn(self):
        self.handleInput()
        for index,button in enumerate(self.buttons):
            self.screen.blit(button[ButtonData.Sprite] if index != self.selectionIndex else button[ButtonData.SpriteSelected],
                             button[ButtonData.Position])


        self.playerSelectionRect.x = 52+(160*self.selectionIndex)   
        self.screen.blit(self.playerSelectionSprite,self.playerSelectionRect)

    def enemyTurn(self):
        for sprites in self.visibleSprites:
            self.screen.blit(sprites.sprite,sprites.rect.center)


    def update(self):      
        getCurrentTurn = self.turns.get(self.currentTurn)
        getCurrentTurn()
    
        self.player.update()
