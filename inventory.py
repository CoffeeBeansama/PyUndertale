import pygame as pg

class InventorySlot:
    def __init__(self,pos,item,index):
        self.screen = pg.display.get_surface()

        self.pos = pos

        self.index = index

        self.data = item

        
