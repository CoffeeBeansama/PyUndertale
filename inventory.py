import pygame as pg
from support import drawBox
from eventHandler import EventHandler
from timer import Timer

class InventorySlot:
    def __init__(self,pos,item,index):
        self.screen = pg.display.get_surface()

        self.pos = pos

        self.index = index

        self.data = item

class Inventory:
    def __init__(self):
        
        self.screen = pg.display.get_surface()
        self.timer = Timer(300)
        self.renderInventory = False
    
        self.xPos,self.yPos = 25,80
        self.width,self.height = 250,350
        
    
    

    def handleKeyBoardInput(self):
        if EventHandler.pressingInventoryButton() and not self.timer.activated:
           self.renderInventory = True if not self.renderInventory else False
           self.timer.activate()

    def handleRendering(self):
        if not self.renderInventory : return 

        inventoryBackground = drawBox(self.screen,self.xPos,self.yPos,self.width,self.height)

    def update(self):
        self.timer.update()
        self.handleKeyBoardInput()
        self.handleRendering()
