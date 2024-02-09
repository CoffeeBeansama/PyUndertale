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
        self.initializeBattleInventory()

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
    
    def initializeBattleInventory(self):

        # Background
        self.battle_XPos,self.battle_YPos = 88,220
        self.battle_Width,self.battle_Height = 500,150

        # ItemSlots
        self.battle_Slot_XPos = 110
        self.battle_Slot_YPos = 245
        
        self.battle_Offset = 45

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
           if self.selectionIndex < self.maxItemCapacity - 1:
              self.selectionIndex += 1
              self.timer.activate()
        
        if EventHandler.pressingInteractButton():
           item = self.itemSlots[self.selectionIndex].data
           if item is not None:
              self.useSelectedItem(item)
              self.timer.activate()
    
    def useSelectedItem(self,item):
        if not self.renderInventory: return
        print(item)
    
    def getSlotPosition(self,slot):
        if self.selectionIndex in range(0,4):
           if slot.index in range(2,4):
              x = self.battle_Slot_XPos + 250
              y = self.battle_Slot_YPos + ((slot.index -2) * self.battle_Offset)
           elif slot.index in range(0,2):
              x = self.battle_Slot_XPos 
              y = self.battle_Slot_YPos + (slot.index * self.battle_Offset)   
        elif self.selectionIndex in range(4,8):
           if slot.index in range(6,8):
              x = self.battle_Slot_XPos + 250
              y = self.battle_Slot_YPos + ((slot.index - 6) * self.battle_Offset)
           elif slot.index in range(4,6):
              x = self.battle_Slot_XPos 
              y = self.battle_Slot_YPos + ((slot.index - 4) * self.battle_Offset)

        return (x,y)
    
    def openBattleInventory(self):
        self.renderInventory = True
        self.selectionIndex = 0
    def closeBattleInventory(self):
        self.renderInventory = False
        self.selectionIndex = 0

    def handleBattleInventory(self):
        self.handleKeyBoardInput()
        self.timer.update()

        background = drawBox(self.screen,self.battle_XPos,self.battle_YPos,self.battle_Width,self.battle_Height)

        for slot in self.itemSlots:
            try:               
               slots = self.screen.blit(self.getItemText(slot),self.getSlotPosition(slot))
            except: pass

    def getItemText(self,slot):
        if self.selectionIndex == slot.index:
           return self.font.render(f">{slot.data}<" if slot.data is not None else ">-------<",True,self.fontColor)
        else:
           return self.font.render(f"{slot.data}" if slot.data is not None else " -------",True,self.fontColor)

    def handleRendering(self):
        if not self.renderInventory : return 
        inventoryBackground = drawBox(self.screen,self.xPos,self.yPos,self.width,self.height)
        
        for slot in self.itemSlots:
            self.screen.blit(self.getItemText(slot),slot.position)

    def update(self):
        self.timer.update()
        self.handleKeyBoardInput()
        self.handleRendering()
