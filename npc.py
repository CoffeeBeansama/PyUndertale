import pygame as pg
from support import loadSprite

class NPC(pg.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        self.spritePath = "Sprites/Npc/Overworld/"

    
    def interact(self):
        print("interacted")

    
    def disengage(self):pass


class Papyrus(NPC):
    def __init__(self,pos,group,dialogue):
        super().__init__(group)

        self.sprite = loadSprite(f"{self.spritePath}Papyrus.png",(25,42))
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)


     