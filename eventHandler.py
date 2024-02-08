import pygame as pg

class EventHandler(object):
    pressingUp = False
    pressingDown = False
    pressingRight = False
    pressingLeft = False
    pressingInteract = False
    pressingInventory = False
    pressingClose = False

    @staticmethod
    def handlePlayerInput():
        keys = pg.key.get_pressed()

        EventHandler.pressingUp = True if keys[pg.K_UP] else False
        EventHandler.pressingDown = True if keys[pg.K_DOWN] else False
        EventHandler.pressingRight = True if keys[pg.K_RIGHT] else False
        EventHandler.pressingLeft = True if keys[pg.K_LEFT] else False
        EventHandler.pressingInteract = True if keys[pg.K_x] else False
        EventHandler.pressingInventory = True if keys[pg.K_z] else False
        EventHandler.pressingClose = True if keys[pg.K_c] else False

    def pressingUpButton():
        return EventHandler.pressingUp
    
    def pressingDownButton():
        return EventHandler.pressingDown
    
    def pressingRightButton():
        return EventHandler.pressingRight
    
    def pressingLeftButton():
        return EventHandler.pressingLeft
    
    def pressingInteractButton():
        return EventHandler.pressingInteract

    def pressingInventoryButton():
        return EventHandler.pressingInventory

    def pressingCloseButton():
        return EventHandler.pressingClose
