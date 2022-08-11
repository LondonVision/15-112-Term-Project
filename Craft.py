import copy
from Block import *
class Craft(object):
    def __init__(self):
        self.recipes = {"dirtdirtdirtdirt":(copy.deepcopy(Block("packed dirt",10,"PeachPuff4")),2),
                        "stonedirtdirtstone":(copy.deepcopy(Block("dirt stone",15,"salmon4")),2),
                        "iron oreiron oreiron oreiron ore":(copy.deepcopy(Block("iron",20,"LightCyan3")),1),
                        "gold oregold oregold oregold ore":(copy.deepcopy(Block("gold",10,"gold")),1),
                        "diamond orediamond orediamond orediamond ore":(copy.deepcopy(Block("diamond",25,"cyan2")),1)}