import pygame as pg
from support import drawBox
from eventHandler import EventHandler
from timer import Timer

class InventorySlot:
    def __init__(self,position,index,data):
        self.position = position
        self.index = index
        self.data = data


class Inventory:
    def __init__(self):
        
        self.screen = pg.display.get_surface()
        self.timer = Timer(300)
        self.renderInventory = False
    
        self.xPos,self.yPos = 25,80
        self.width,self.height = 250,350
       
        self.initializeItemSlots()

        self.selectionIndex = 0
        
    def initializeItemSlots(self):    
        self.maxItemCapacity = 8
        self.itemSlots = []

        self.slot_XPos = 50

        slotStart_YPos = 90
        
        slot_Y_Offset = 40

    
        for index in range(self.maxItemCapacity):
            yPos = slotStart_YPos + (index * slot_Y_Offset)
            newSlot = InventorySlot((self.slot_XPos,yPos),index,None)
            self.itemSlots.append(newSlot)

        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",40)
        self.fontColor = (255, 255, 255)

    def handleKeyBoardInput(self):
        if self.timer.activated: return

        if EventHandler.pressingInventoryButton():
           self.renderInventory = True if not self.renderInventory else False
           self.selectionIndex = 0 if self.renderInventory else 0
           self.timer.activate()

        if EventHandler.pressingUpButton():
           if self.selectionIndex > 0:
              self.selectionIndex -= 1
              self.timer.activate()

        if EventHandler.pressingDownButton():
           if self.selectionIndex < self.maxItemCapacity:
              self.selectionIndex += 1
              self.timer.activate()
        
        if EventHandler.pressingInteractButton():
           item = self.itemSlots[self.selectionIndex].data
           if item is not None:
              self.useSelectedItem(item)
              self.timer.activate()
    
    def useSelectedItem(self,item):
        print(item)

    def handleRendering(self):
        if not self.renderInventory : return 
        inventoryBackground = drawBox(self.screen,self.xPos,self.yPos,self.width,self.height)
        
        for slot in self.itemSlots:
            if self.selectionIndex == slot.index:
              itemText = self.font.render(f">{slot.data}<" if slot.data is not None else ">-------<",True,self.fontColor)

            else:
              itemText = self.font.render(f"{slot.data}" if slot.data is not None else " -------",True,self.fontColor)
            self.screen.blit(itemText,slot.position)

    def update(self):
        self.timer.update()
        self.handleKeyBoardInput()
        self.handleRendering()
