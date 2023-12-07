import pygame as pg
from enum import Enum
from scene import Scene
from timer import Timer
from settings import GameData
from player import PlayerSoul
from support import loadSprite
from eventHandler import EventHandler


class Turn(Enum):
    PlayerTurn = "Player Turn"
    EnemyTurn = "Enemy Turn"

class ButtonData(Enum):
     Sprite = "Sprite"
     SpriteSelected = "Selected Sprite"
     Position = "Position"
     Event = "Function Event"

class Battle(Scene):
    
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)
        self.visibleSprites = pg.sprite.Group()
        self.eventHandler = EventHandler()
        

        self.player = PlayerSoul((100,100),self.visibleSprites,self.collisionSprites)
        

        self.currentTurn = Turn.PlayerTurn
        self.turns = {
            Turn.PlayerTurn : self.playerTurn,
            Turn.EnemyTurn : self.enemyTurn
        }

        self.selectionIndex = 0
        self.buttonPressedTimer = Timer(150)
               
        self.currentRender = ""
        self.renderSelection = {
            "Target" : self.renderTargetSprite,
            "Items" : self.renderInventoryItems
        }
        

        self.currentEnemy = None
        
        self.createButtons()

        self.createPlayerHUD()
        
        self.createPlayerAttack()
            
        self.createSliceAnimation()
        
    def createPlayerHUD(self):
        self.spritePath = "Sprites/Player/"
        self.playerSelectionSprite = loadSprite(f"{self.spritePath}PlayerSoul.png",(20,20))
        self.playerSelectionStartXPos = 71
        startingPos = (self.playerSelectionStartXPos,445)
        self.playerSelectionRect = self.playerSelectionSprite.get_rect(topleft=startingPos)
  
        self.playerHudfont = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",38)
        self.fontColor = (255, 255, 255)
    
    def createPlayerAttack(self):
        # Target Board
        self.drawTargetSprite = False
        self.targetSpriteSize = (546,115)
        self.targetSprite = loadSprite(f"Sprites/target.png",self.targetSpriteSize)
        self.targetSpriteRect = self.targetSprite.get_rect(topleft=(60,250))
  
        # Target Bar
        size = (14,128)
        self.targetChoiceStartPos = (590,243)
        self.currentTargetPos = 590
        self.targetSelected = False
  
        self.targetChoiceSprite = {
            "Start" : loadSprite("Sprites/targetChoice.png",size),
            "Set" : loadSprite("Sprites/targetChoice2.png",size)
        }
        self.currentTargetChoiceSprite = self.targetChoiceSprite["Start"]

    def createButtons(self):
        spritePath = "Sprites/UI/"
        buttonSize = (140,70)

        self.playerButton = {
            "Fight": { ButtonData.Event : self.fightButton },
            "Item": { ButtonData.Event : self.itemButton },
            "Mercy": { ButtonData.Event : self.mercyButton }
        }

        for i,key in enumerate(self.playerButton.keys()):
             self.playerButton[key][ButtonData.Sprite] = loadSprite(f"{spritePath}{key}Button.png",buttonSize)
             self.playerButton[key][ButtonData.SpriteSelected] = loadSprite(f"{spritePath}{key}ButtonSelected.png",buttonSize)
             self.playerButton[key][ButtonData.Position] = (60+(210*i),420)

        self.buttons = [i for i in self.playerButton.values()]
    
    def createSliceAnimation(self):
        sliceSpritePath = "Sprites/Slash/"
        sliceSpriteSize = (36,120)
        self.slashSprites = {}
        for i in range(0,6):
            self.slashSprites[i] = loadSprite(f"{sliceSpritePath}{i}.png",sliceSpriteSize)
  
        self.frameIndex = 0
        self.slashPos = (310,50)
        self.sliceAnimationTime = 1 / 10

    def uponEnterScene(self):
        self.selectionIndex = 0
        self.currentEnemy = self.game.gameData[GameData.CurrentEnemy]

        # Preventing from double pressing the fight button when entering scene
        if not self.buttonPressedTimer.activated:
            self.buttonPressedTimer.activate()
              

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
                
                if self.currentTargetPos < 580:
                   self.targetSelected = True
                   self.currentTargetChoiceSprite = self.targetChoiceSprite["Set"]
                   
            self.buttonPressedTimer.activate()    


        if self.selectionIndex < 0:
             self.selectionIndex = 0

        if self.selectionIndex > len(self.buttons) -1:
             self.selectionIndex = int(len(self.buttons)) - 1
    

    def fightButton(self):
        self.currentRender = "Target"
        
    
    def itemButton(self):
        print("item")

    def mercyButton(self):
        self.switchScene(self.sceneCache.overWorld())

    def damageEnemy(self,pos):
        if pos <= 350 and pos >= 315:
           print("Perfect!!")
        elif pos <= 435 and pos >= 316:
           print("Great Timing!!")
        elif pos <= 314 and pos >= 235:
           print("Great Timing!!")
        else:
           print("Missed!!")


    def playerTurn(self):
        self.handleInput()

        self.animateSliceAnimation()

        try:
            renderSelected = self.renderSelection.get(self.currentRender)
            renderSelected()
 
        except: pass

    
    def renderTargetSprite(self):     
        white = (255,255,255)
        offset = 5
        pg.draw.rect(self.screen,white,
                    (self.targetSpriteRect.x-offset,self.targetSpriteRect.y-offset,
                    self.targetSpriteSize[0]+(offset*2),self.targetSpriteSize[1]+(offset*2)))
        
        black = (0,0,0)
        pg.draw.rect(self.screen,black,
                    (self.targetSpriteRect.x,self.targetSpriteRect.y,
                    self.targetSpriteSize[0],self.targetSpriteSize[1]))

        self.screen.blit(self.targetSprite,self.targetSpriteRect)
        
        if self.currentTargetPos >= 60:
           if not self.targetSelected:
              self.currentTargetPos -= 5

        self.screen.blit(self.currentTargetChoiceSprite,(self.currentTargetPos,self.targetChoiceStartPos[1]))
    
    def renderInventoryItems(self): 
        pass
    
    def renderPlayerHUD(self):
        playerName = self.playerHudfont.render(self.player.name,True,self.fontColor)
        self.screen.blit(playerName,(50,375))

        playerLV = self.playerHudfont.render(f"LV{self.player.levelOfViolence}",True,self.fontColor)
        self.screen.blit(playerLV,(215,375))

        hpText = self.playerHudfont.render("HP",True,self.fontColor)
        self.screen.blit(hpText,(290,375))

        xPos = 340
        yPos = 380
        maxWidth = 100
        height = 30

        red = (255,0,0)
        hpBarBackGround = pg.draw.rect(self.screen,red,(xPos,yPos,maxWidth,height))

        yellow = (255, 255, 0)
        diff = (maxWidth / self.player.maxHP) * maxWidth
        playerHPBarWidth = (self.player.currentHP / maxWidth) * diff
        playerHPBar = pg.draw.rect(self.screen,yellow,(xPos,yPos,playerHPBarWidth,height))

        playerHp = self.playerHudfont.render(f"{self.player.currentHP}/{self.player.maxHP}",True,self.fontColor)
        self.screen.blit(playerHp,(470,375))



    def enemyTurn(self):
        for sprites in self.visibleSprites:
            self.screen.blit(sprites.sprite,sprites.rect.center)

    def animateSliceAnimation(self):
        if not self.targetSelected: return
        self.frameIndex += self.sliceAnimationTime

        if self.frameIndex >= len(self.slashSprites):
           self.targetSelected = False
           self.damageEnemy(self.currentTargetPos)
           self.currentTurn = Turn.EnemyTurn
           self.frameIndex = 0

        self.screen.blit(self.slashSprites[int(self.frameIndex)],self.slashPos)

        

    def update(self):
        getCurrentTurn = self.turns.get(self.currentTurn)
        getCurrentTurn()
        
        
        for index,button in enumerate(self.buttons):
            self.screen.blit(button[ButtonData.Sprite] if index != self.selectionIndex else button[ButtonData.SpriteSelected],button[ButtonData.Position])

        self.playerSelectionRect.x = self.playerSelectionStartXPos+(210*self.selectionIndex)
        self.screen.blit(self.playerSelectionSprite,self.playerSelectionRect)

        self.renderPlayerHUD()
        self.player.update()


