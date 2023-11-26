
from enum import Enum
from overworld import OverWorld
from battle import Battle

class Scenes(Enum):
    OverWorld = 1,
    Battle = 2
    
class SceneCache:
    def __init__(self,game):
        
        self.scenes = {
            Scenes.OverWorld : OverWorld(self,game),
            Scenes.Battle : Battle(self,game),
        }

    def overWorld(self):
        return self.scenes[Scenes.OverWorld]
    
    def battle(self):
        return self.scenes[Scenes.Battle]