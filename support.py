import pygame as pg
from os import walk
from csv import reader


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    paths = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            paths.append(full_path)

        paths.sort(key=lambda x: x[-4:-2])
        for element in paths:
            image_surf = pg.image.load(element).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def drawBox(surface,xPos, yPos, width, height):
    white = (255,255,255)
    black = (0,0,0)
    # Background
    pg.draw.rect(surface, white, (xPos, yPos, width, height))
    
    box = pg.draw.rect(surface, black, (xPos + 5, yPos + 5, width - 10, height - 10))

    return box

def loadSprite(imagePath, scale):
    newImage = pg.transform.scale(pg.image.load(imagePath),scale).convert_alpha()
    return newImage
