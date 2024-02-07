import pygame as pg
from support import loadSprite
from attackmanager import *

class NPC(pg.sprite.Sprite):
    def __init__(self,group,dialogueSystem):
        super().__init__(group)

        self.maxHP = 20
        self.currentHP = self.maxHP
        
        self.interactActed = False
        self.dialogueSystem = dialogueSystem
        self.spritePath = "Sprites/Npc/Overworld/"
        
    
    def reduceHp(self,amount):
        self.currentHP -= amount
    
    def interact(self):
        if not self.interactActed:
            self.dialogueSystem.startDialogue(self.dialogueID)
            self.interactActed = True

    
    def disengage(self):
        if self.interactActed:
            self.interactActed = False


class Papyrus(NPC):
    def __init__(self,pos,group,dialogueSystem):
        super().__init__(group,dialogueSystem)

        self.dialogueID = "Papyrus"
        
        self.sprite = loadSprite(f"{self.spritePath}Papyrus.png",(25,42))
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)
        
        self.battleSprite = loadSprite(f"{self.spritePath}PapyrusBattle.png",(154,184))
        self.battleSprite.set_alpha(240)
        self.battleSpriteRect = self.battleSprite.get_rect(topleft=(260,30))

        self.attack = PapyrusAttack()
        
