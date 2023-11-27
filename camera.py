import pygame as pg

#region
class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_canvas = pg.display.get_surface()
        self.half_width = self.display_canvas.get_size()[0] // 2
        self.half_height = self.display_canvas.get_size()[1] // 2

        
        self.internalSurfaceSize = (300, 300)
        self.internalSurface = pg.Surface(self.internalSurfaceSize, pg.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center=(self.half_width, self.half_height))
        self.offset_rect = None
        self.zoomInSize = (700, 650)

        self.internalOffset = pg.math.Vector2()
        self.internalOffset.x = self.internalSurfaceSize[0] // 2 - self.half_width
        self.internalOffset.y = self.internalSurfaceSize[1] // 2 - self.half_height

        self.offset = pg.math.Vector2()
        self.textOffset = pg.math.Vector2()

        

    def custom_draw(self, player):
        # getting the offset  for camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.internalSurface.fill("black")
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.offset_rect = sprite.rect.topleft - self.offset + self.internalOffset
            self.internalSurface.blit(sprite.sprite, self.offset_rect)

        scaledSurface = pg.transform.scale(self.internalSurface, self.zoomInSize)
        self.scaledRect = scaledSurface.get_rect(center=(self.half_width, self.half_height))
        self.display_canvas.blit(scaledSurface, self.scaledRect)

#endregion
