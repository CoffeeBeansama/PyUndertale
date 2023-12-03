from overworld import OverWorld
from battle import Battle


class SceneCache:
    def __init__(self,game):
        self.scenes = {
            "OverWorld" : OverWorld(self,game),
            "Battle" : Battle(self,game),
        }

    def overWorld(self):
        return self.scenes["OverWorld"]
    
    def battle(self):
        return self.scenes["Battle"]