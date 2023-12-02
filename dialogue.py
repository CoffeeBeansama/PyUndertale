import pygame as pg
from support import *
from timer import Timer
from eventHandler import EventHandler
from pygame import mixer


dialogues = {
    "Papyrus": {
        1: ["Papyrus",'Well hello there!'],
    }
}


class DialogueSystem:
    def __init__(self,player):
        self.player = player
        self.screen = pg.display.get_surface()

        self.eventHandler = EventHandler()
        
        self.renderedText = {}

        self.textToMove = []

        self.textStartPos = [200, 200]
    
        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",36)
        self.fontColor = (255, 255, 255)

        self.letterSprites = None
        self.currentSpeaker = None
        self.lastSpace = None

        self.faceSpriteScale = (75,75)
        self.faceSpritePos = (70,475)
        self.speakerNameTextPos = (74,562)
        self.faceFrameIndex = 0

        
        self.dialogueIndex = 1
        self.charIndex = 0

        self.ticked = False
        self.typingSpeedTimer = Timer(35,self.unTick)

        self.xStartText = 190
        self.textXPos = self.xStartText
        self.xDistanceBetween = 18
        self.maximumXTextXBounds = 740

        self.yStartText = 400
        self.textYPos = self.yStartText
        self.textYOffset = 26
        self.maximumXTextYBounds = 531

        self.keyPressedCount = 0
        self.skipKeyPressed = False
        self.skipTimer = Timer(50,lambda : self.skipKeyPressed == False)

        self.buttonPressedTime = None

        self.lineCut = False
        self.dialogueActive = False
        
        self.lineFinished = False
        self.skippedDialogue = False

   
    def startDialogue(self,speaker):
        self.currentSpeaker = speaker
        self.charIndex = 0
        self.dialogueActive = True
        self.skippedDialogue = False
      

    def endDialogue(self):
        self.dialogueIndex = 1
        self.currentSpeaker = None
        self.dialogueActive = False


    def checkPlayerInput(self):
        self.eventHandler.handlePlayerInput()
        self.skipTimer.update()

        if self.eventHandler.pressingInteractButton():
            if not self.skipTimer.activated:
                if self.lineFinished:
                    self.nextDialogue()
                else:
                    self.skippedDialogue = True
                self.skipTimer.activate()
                


    def checkSkipDialogue(self):
        if not self.skippedDialogue:
            return
        self.typingSpeed = 0

    def nextDialogue(self):
        self.charIndex = 0
        self.dialogueIndex += 1
        self.textXPos = self.xStartText
        self.textYPos = self.yStartText
        self.renderedText.clear()
        self.lineFinished = False
        self.typingSpeed = 35
        self.skippedDialogue = False


        
    def addTextToRender(self, txt):
        if self.lineFinished : return

        if self.charIndex >= len(txt):
            self.lineFinished = True
            return
        
        if not self.lineCut:
            if not self.ticked:
                self.ticked = True
                for i in range(len(txt)):
                    characterSprite = self.font.render(txt[self.charIndex],True,self.fontColor)
                    currentTxt = txt[self.charIndex]

                    self.renderedText[f"{currentTxt}{self.charIndex}"] = {
                            "LetterSprite": characterSprite,
                            "XPos": self.textXPos,
                            "YPos": self.textYPos,
                            "LetterStored": txt[self.charIndex],
                            "IndexPos": self.charIndex
                            }
                    self.textXPos += self.xDistanceBetween
                    self.charIndex += 1
                    return



    def fixOutOfBoundsText(self):
        self.textXPos = self.xStartText
        self.textYPos += self.textYOffset
        for textIndex, text in enumerate(reversed(self.renderedText.values())):
            if text["LetterStored"] != " ":
                self.textToMove.append(text)
            else:
                reversedInt = self.textToMove[::-1]
                for index, texts in enumerate(reversedInt):
                    newTextXOffset = self.xStartText + (index * self.xDistanceBetween)
                    texts["XPos"] = newTextXOffset
                    texts["YPos"] += self.textYOffset
                    self.textXPos = newTextXOffset + self.xDistanceBetween
                self.textToMove.clear()
                self.lineCut = False
                return

    def checkTextOutOfBounds(self):
        if self.textYPos <= self.maximumXTextYBounds:
            if self.textXPos > self.maximumXTextXBounds:
                self.lineCut = True
                self.fixOutOfBoundsText()
        else:
            self.textXPos = self.xStartText
            self.textYPos = self.yStartText
            self.renderedText.clear()

    def unTick(self):
        self.ticked = False

    def display(self):
        self.typingSpeedTimer.update()
        
        self.checkPlayerInput()

        if self.ticked:
            if not self.typingSpeedTimer.activated:
                self.typingSpeedTimer.activate()

        if self.currentSpeaker is not None:
            if self.dialogueIndex <= len(dialogues[self.currentSpeaker]):

                self.checkSkipDialogue()
                self.checkTextOutOfBounds()
                self.addTextToRender(dialogues[self.currentSpeaker][self.dialogueIndex][1])
            else:
                self.endDialogue()

            for text in self.renderedText.values():
                self.screen.blit(text["LetterSprite"], (text["XPos"], text["YPos"]))