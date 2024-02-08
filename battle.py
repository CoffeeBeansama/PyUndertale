import pygame as pg
from enum import Enum
from scene import Scene
from timer import Timer
from support import import_csv_layout
from tile import WallTile
from settings import GameData
from player import PlayerSoul
from support import loadSprite,drawBox
from eventHandler import EventHandler
from attackobj import BoneObject
import random

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

        self.currentTurn = Turn.PlayerTurn
        self.turns = {
            Turn.PlayerTurn : self.playerTurn,
            Turn.EnemyTurn : self.enemyTurn
        }

        self.selectionIndex = 0
        self.buttonPressedTimer = Timer(150)
        
        self.enemyAttackTimer = Timer(8000,self.onEnemyAttackEnd)

        self.currentRender = ""
        self.renderSelection = {
            "Target" : self.renderTargetSprite,
            "Enemy HP" : self.handleDamageEnemy, 
            "Items" : self.renderInventoryItems
        }
        
        
        self.currentEnemy = None
        self.currentEnemyAttack = None 

        self.createButtons()

        self.createPlayerHUD()
        
        self.createPlayerAttack()
            
        self.createSliceAnimation()

        self.createBorders()
        

        self.initializePlayerHPBar()
        self.initializeEnemyHPBar()

        self.player = PlayerSoul((100,100),self.visibleSprites,self.collisionSprites)

        
        self.enemyDamageTimer = Timer(2000,self.startEnemyTurn)
        self.enemyFlashTimer = Timer(400)

        self.currentEnemySpriteAlpha = 1

        self.enemySpriteAlpha = {
            1 : 255,
            -1 : 180
        }


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

    def initializePlayerHPBar(self):    
        self.playerHPBar_XPos = 340
        self.playerHPBar_YPos = 380
        self.playerHPBar_maxWidth = 100
        self.playerHPBar_height = 30

    def initializeEnemyHPBar(self): 
        self.enemyHPBar_XPos = 210
        self.enemyHPBar_YPos = 230
        self.enemyHPBar_maxWidth = 250
        self.enemyHPBar_maxHeight = 20
        self.tempEnemyHPBar_Width = 0        
        
        self.enemyDamageHUDText = ""
        self.enemyDamagefont = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",40)

    def createSliceAnimation(self):
        sliceSpritePath = "Sprites/Slash/"
        sliceSpriteSize = (36,120)
        self.slashSprites = {}
        for i in range(0,6):
            self.slashSprites[i] = loadSprite(f"{sliceSpritePath}{i}.png",sliceSpriteSize)
  
        self.frameIndex = 0
        self.slashPos = (310,50)
        self.sliceAnimationTime = 1 / 10
    
    def createBorders(self):
        layout = {
        "border" : import_csv_layout("Map/playerBounds.csv"),
        "background" : import_csv_layout("Map/background.csv"),
        }
        
        tilesize = 12

        for style,layouts in layout.items():
            for rowIndex,row in enumerate(layouts):
                for columnIndex,column in enumerate(row):

                    if column != "-1":
                       x = columnIndex * tilesize - (tilesize * 2)
                       y = rowIndex * 12 - (tilesize * 2)

                       if style == "border":
                          WallTile(loadSprite(f"Sprites/wall.png",(tilesize*2,tilesize*2)),(x,y),[self.visibleSprites,self.collisionSprites])

                       if style == "background":
                          WallTile(loadSprite(f"Sprites/Background.png",(tilesize*2,tilesize*2)),(x,y),[self.visibleSprites])


    def uponEnterScene(self):
        self.currentRender = ""
        self.selectionIndex = 0
        self.currentEnemy = self.game.gameData[GameData.CurrentEnemy]

        
        diff = (self.enemyHPBar_maxWidth / self.currentEnemy.maxHP) * self.enemyHPBar_maxWidth
        self.tempEnemyHPBar_Width = (self.currentEnemy.currentHP / self.enemyHPBar_maxWidth) * diff

        # Preventing from double pressing the fight button when entering scene
        if not self.buttonPressedTimer.activated:
            self.buttonPressedTimer.activate()
              

    def handleInput(self):
        if self.currentRender == "Enemy HP": return
        if not self.buttonPressedTimer.activated:

            if EventHandler.pressingRightButton():
                self.selectionIndex += 1
            if EventHandler.pressingLeftButton():
                self.selectionIndex -= 1

            if EventHandler.pressingInteractButton():
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
        self.currentTargetChoiceSprite = self.targetChoiceSprite["Start"]
        self.currentRender = "Target"
        
    
    def itemButton(self):
        pass

    def mercyButton(self):
        self.currentRender = ""
        self.selectionIndex = 0
        self.currentEnemy = None
        # Preventing from double pressing the fight button when entering scene
        if not self.buttonPressedTimer.activated:
            self.switchScene(self.sceneCache.overWorld())
            self.buttonPressedTimer.activate()


    def damageEnemy(self,pos):
        if pos <= 350 and pos >= 315:
           self.enemyDamageHUDText = f"Perfect!"
           self.currentEnemy.reduceHp(self.player.currentDamage)   
        elif pos <= 435 and pos >= 316 or pos <= 314 and pos >= 235:   
           self.enemyDamageHUDText = f"Great!"
           self.currentEnemy.reduceHp(self.player.currentDamage * .80)   
        else:
           self.enemyDamageHUDText = "Missed!"
           self.currentEnemy.reduceHp(0)   


    def playerTurn(self):
        self.enemyFlashTimer.update()
        self.enemyDamageTimer.update()

        self.handleInput()
        self.animateSliceAnimation()

        
        renderSelected = self.renderSelection.get(self.currentRender)
        if renderSelected:
           renderSelected()
        
    
    def startEnemyTurn(self):
        self.currentTurn = Turn.EnemyTurn
        self.currentEnemy.battleSprite.set_alpha(self.enemySpriteAlpha[1])
    
    def drawHPBar(self,x,y,width,maxWidth,height): 
        red = (255,0, 0)
        yellow = (255, 255, 0)

        pg.draw.rect(self.screen,red,(x,y,maxWidth,height))
        return pg.draw.rect(self.screen,yellow,(x,y,width,height))

    def handleDamageEnemy(self):

        diff = (self.enemyHPBar_maxWidth / self.currentEnemy.maxHP) * self.enemyHPBar_maxWidth 
        enemyHPBarWidth = (self.currentEnemy.currentHP / self.enemyHPBar_maxWidth) * diff
        if self.tempEnemyHPBar_Width > enemyHPBarWidth:
           self.tempEnemyHPBar_Width -= 0.90

        enemyHPBar = self.drawHPBar(self.enemyHPBar_XPos,self.enemyHPBar_YPos,enemyHPBarWidth,self.enemyHPBar_maxWidth,self.enemyHPBar_maxHeight) 
        tempEnemyHPBar = pg.draw.rect(self.screen,(255,255,0),(self.enemyHPBar_XPos,self.enemyHPBar_YPos,self.tempEnemyHPBar_Width,20))
        
        playerDamage = self.enemyDamagefont.render(self.enemyDamageHUDText,True,self.fontColor)
        self.screen.blit(playerDamage,(430,70))

        if not self.enemyFlashTimer.activated:
           self.currentEnemySpriteAlpha *= -1
           self.currentEnemy.battleSprite.set_alpha(self.enemySpriteAlpha[self.currentEnemySpriteAlpha])
           self.enemyFlashTimer.activate()
    
    def renderTargetSprite(self):            
        drawBox(self.screen,self.targetSpriteRect.x,self.targetSpriteRect.y,
                self.targetSpriteSize[0],self.targetSpriteSize[1])

        self.screen.blit(self.targetSprite,self.targetSpriteRect)
        
        maximumXPos = 60
        if self.currentTargetPos >= maximumXPos:
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

        diff = (self.playerHPBar_maxWidth / self.player.maxHP) * self.playerHPBar_maxWidth
        playerHPBarWidth = (self.player.currentHP / self.playerHPBar_maxWidth) * diff
        playerHPBar = self.drawHPBar(self.playerHPBar_XPos,self.playerHPBar_YPos,playerHPBarWidth,
                                    self.playerHPBar_maxWidth,self.playerHPBar_height)

        playerHp = self.playerHudfont.render(f"{self.player.currentHP}/{self.player.maxHP}",True,self.fontColor)
        self.screen.blit(playerHp,(470,375))



    def enemyTurn(self):
        if not self.enemyAttackTimer.activated:
           self.currentEnemyAttack = random.choice(list(self.currentEnemy.attack.attacks.values()))
           self.enemyAttackTimer.activate()
        
        for projectile in self.currentEnemy.attack.projectiles:
            if projectile.obj:
               if projectile.obj.collidepoint(self.player.rect.center):
                  self.player.damagePlayer(projectile.damage)


        for sprites in self.visibleSprites:
            self.screen.blit(sprites.sprite,sprites.rect.center)
        
        if self.currentEnemyAttack: 
           self.currentEnemyAttack()
        
        self.player.update()
        self.enemyAttackTimer.update()

    def onEnemyAttackEnd(self):
        self.currentRender = "" 
        self.currentTargetPos = self.targetChoiceStartPos[0]
        self.currentEnemy.attack.projectiles.clear()
        self.currentEnemyAttack = None
        
        self.currentTurn = Turn.PlayerTurn

    def animateSliceAnimation(self):
        if not self.targetSelected: return
        self.frameIndex += self.sliceAnimationTime

        if self.frameIndex >= len(self.slashSprites):
           if not self.enemyDamageTimer.activated:
              self.enemyDamageTimer.activate()

           self.targetSelected = False
           self.damageEnemy(self.currentTargetPos)
           self.currentRender = "Enemy HP"
           self.frameIndex = 0

        self.screen.blit(self.slashSprites[int(self.frameIndex)],self.slashPos)

        

    def update(self):
        self.screen.blit(self.currentEnemy.battleSprite,self.currentEnemy.battleSpriteRect)
            
        getCurrentTurn = self.turns.get(self.currentTurn)
        getCurrentTurn()
        

        for index,button in enumerate(self.buttons):
            self.screen.blit(button[ButtonData.Sprite] if index != self.selectionIndex else button[ButtonData.SpriteSelected],button[ButtonData.Position])

        self.playerSelectionRect.x = self.playerSelectionStartXPos+(210*self.selectionIndex)
        self.screen.blit(self.playerSelectionSprite,self.playerSelectionRect)
        
        self.renderPlayerHUD()
    


