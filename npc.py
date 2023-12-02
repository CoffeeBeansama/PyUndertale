import pygame as pg
from support import loadSprite

class NPC(pg.sprite.Sprite):
    def __init__(self,group,dialogueSystem):
        super().__init__(group)

        self.dialogueSystem = dialogueSystem
        self.spritePath = "Sprites/Npc/Overworld/"

    
    def interact(self):
        self.dialogueSystem.startDialogue(self.dialogueID)

    
    def disengage(self):pass


class Papyrus(NPC):
    def __init__(self,pos,group,dialogueSystem):
        super().__init__(group,dialogueSystem)

        self.dialogueID = "Papyrus"

        self.sprite = loadSprite(f"{self.spritePath}Papyrus.png",(25,42))
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)


     