import pygame as pg
from scene import Scene
from player import Frisk
from camera import CameraGroup
from tile import WallTile
from support import import_csv_layout
from settings import GameData,tileSize
from dialogue import DialogueSystem,dialogues
from npc import *
from inventory import Inventory

class OverWorld(Scene):
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)

        self.visibleSprites = CameraGroup()
        self.npcSprites = pg.sprite.Group()

        self.player = Frisk((270,300),self.visibleSprites,self.collisionSprites,self.npcSprites,self.enterBattleScene)


        self.dialogueSystem = DialogueSystem(self.player,self.enterBattleScene)

        self.npcs = {
            "Papyrus" : Papyrus((300,230),[self.npcSprites,self.visibleSprites],self.dialogueSystem)
        }
         
        self.createMap()
   
        self.playerInventory = Inventory()

    def createMap(self):
        mapLayouts = {
            "Wall" : import_csv_layout("Map/Wall.csv"),
            "SpawnArea": import_csv_layout("Map/SpawnArea.csv")
        }

        for style, layout in mapLayouts.items():
            for rowIndex, row in enumerate(layout):
                for columnIndex, column in enumerate(row):

                    if column != "-1":
                        x = columnIndex * tileSize
                        y = rowIndex * tileSize
                        
                        if style == "Wall":
                           WallTile(loadSprite(f"Sprites/wall.png",(32,32)),(x,y),[self.visibleSprites,self.collisionSprites])

                        
    def uponEnterScene(self):
        self.game.gameData[GameData.CurrentEnemy] = None
        
    def enterBattleScene(self,npc):
        self.game.gameData[GameData.CurrentEnemy] = self.npcs[npc]
        self.switchScene(self.sceneCache.battle())
    
    
    def update(self):
        self.player.update()

        self.visibleSprites.custom_draw(self.player)
        self.dialogueSystem.display()
        
        self.playerInventory.update()        

