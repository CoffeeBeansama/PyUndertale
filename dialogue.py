import pygame as pg
from enum import Enum
from support import *
from timer import Timer
from eventHandler import EventHandler
from pygame import mixer


dialogues = {
    "Papyrus": {
        1: 'Well hello there!',
       
    }
}

class LetterData(Enum):
    Surface = "Letter Surface",
    X_Position = "X Position",
    Y_Position = "Y Position",
    Letter = "Actual Letter",
    IndexPosition = "Index Position",


class DialogueSystem:
    def __init__(self,player,startBattle):
        self.player = player
        self.startBattle = startBattle
        self.screen = pg.display.get_surface()

        
        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",36)
        self.fontColor = (255, 255, 255)

        self.currentSpeaker = None
        self.speakerFace_XPos = 45
        self.speakerFace_YPos = 360
        
        self.speakerName_XPos = 40
        self.speakerName_YPos = 440
        self.dialogueIndex = 1
        self.charIndex = 0

        self.ticked = False
        self.typingSpeedTimer = Timer(35,self.unTick)
        self.timer = Timer(200)


        self.xStartText = 180
        self.textXPos = self.xStartText
        self.xDistanceBetween = 18
        self.maximumXTextXBounds = 670

        self.yStartText = 370
        self.textYPos = self.yStartText
        self.textYOffset = 28
        self.maximumXTextYBounds = 450

        self.lineCut = False
        self.dialogueActive = False
        self.lineFinished = False

        self.renderedText = {}
        self.textToMove = []
  

   
    def startDialogue(self,speaker):
        self.currentSpeaker = speaker
        self.charIndex = 0
        self.dialogueActive = True
       
      
    def endDialogue(self):
        self.dialogueIndex = 1
        self.startBattle(self.currentSpeaker.dialogueID)
        self.currentSpeaker = None
        self.dialogueActive = False


    def checkPlayerInput(self):
        self.timer.update()
       
        if EventHandler.pressingInteractButton():
            if not self.timer.activated:
                if self.lineFinished:
                    self.nextDialogue()
                self.timer.activate()
                
    def nextDialogue(self):
        self.charIndex = 0
        self.dialogueIndex += 1
        self.textXPos = self.xStartText
        self.textYPos = self.yStartText
        self.renderedText.clear()
        self.lineFinished = False
       


    def addTextToRender(self,txt):
        if self.charIndex >= len(txt):
            self.lineFinished = True
            return
        
        if not self.ticked:
            letterSurface = self.font.render(txt[self.charIndex],True,self.fontColor)
            currentTxt = txt[self.charIndex]

            self.renderedText[f"{currentTxt}{self.charIndex}"] = {
                    LetterData.Surface: letterSurface,
                    LetterData.X_Position : self.textXPos,
                    LetterData.Y_Position: self.textYPos,
                    LetterData.Letter: txt[self.charIndex],
                    LetterData.IndexPosition : self.charIndex
                    }
            
            self.textXPos += self.xDistanceBetween
            self.charIndex += 1
            self.ticked = True
            return


    def fixOutOfBoundsText(self):
        self.textXPos = self.xStartText
        self.textYPos += self.textYOffset

        for textIndex, text in enumerate(reversed(self.renderedText.values())):
            if text[LetterData.Letter] != " ":
                self.textToMove.append(text)
            else:
                reversedInt = self.textToMove[::-1]
                for index, texts in enumerate(reversedInt):
                    newTextXOffset = self.xStartText + (index * self.xDistanceBetween)
                    texts[LetterData.X_Position] = newTextXOffset
                    texts[LetterData.Y_Position] += self.textYOffset
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

    
    def renderSpeakerName(self):
        name = self.font.render(self.currentSpeaker.dialogueID,True,self.fontColor)
        return self.screen.blit(name,(self.speakerName_XPos,self.speakerName_YPos))

    def display(self):
        self.typingSpeedTimer.update()
        
        self.checkPlayerInput()

        if not self.typingSpeedTimer.activated and self.ticked:
            self.typingSpeedTimer.activate()

        if self.currentSpeaker is not None:
            if self.dialogueIndex <= len(dialogues[self.currentSpeaker.dialogueID]):
                background = drawBox(self.screen,15,350,670,140)
                speakerFace = self.screen.blit(self.currentSpeaker.dialogueSprite,(self.speakerFace_XPos,self.speakerFace_YPos))
                self.renderSpeakerName()
                self.checkTextOutOfBounds()
                self.addTextToRender(dialogues[self.currentSpeaker.dialogueID][self.dialogueIndex])
            else:
                self.endDialogue()

            for text in self.renderedText.values():
                self.screen.blit (text[LetterData.Surface], 
                                 (text[LetterData.X_Position],
                                 text[LetterData.Y_Position]))
