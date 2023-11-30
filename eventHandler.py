import pygame as pg

class EventHandler:

    def handlePlayerInput(self):
        keys = pg.key.get_pressed()

        self.pressingUp = True if keys[pg.K_UP] else False
        self.pressingDown = True if keys[pg.K_DOWN] else False
        self.pressingRight = True if keys[pg.K_RIGHT] else False
        self.pressingLeft = True if keys[pg.K_LEFT] else False
    
    def pressingUpButton(self):
        return self.pressingUp
    
    def pressingDownButton(self):
        return self.pressingDown
    
    def pressingRightButton(self):
        return self.pressingRight
    
    def pressingLeftButton(self):
        return self.pressingLeft