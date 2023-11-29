import pygame as pg
from scene import Scene
from camera import CameraGroup
from player import Frisk
from support import import_csv_layout
from tile import WallTile,SpawnArea
from settings import tileSize

class OverWorld(Scene):
    def __init__(self, sceneCache, game):
        super().__init__(sceneCache, game)

        self.visibleSprites = CameraGroup()
        
        self.spawnArea = pg.sprite.Group()

        self.player = Frisk((270,300),self.visibleSprites,self.collisionSprites,self.spawnArea,self.enterBattleScene)
        self.createMap()
      
            
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
                            WallTile((x,y),[self.visibleSprites,self.collisionSprites])

                        if style == "SpawnArea":
                            SpawnArea((x,y),[self.visibleSprites,self.spawnArea])

    
    def enterBattleScene(self):
        self.switchScene(self.sceneCache.battle())

    def update(self):
        self.player.update()
        self.visibleSprites.custom_draw(self.player)
        

