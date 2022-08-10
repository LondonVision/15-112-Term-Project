import copy
from Block import *
class Craft(object):
    def __init__(self):
        self.recipes = {"dirtdirtdirtdirt":(copy.deepcopy(Block("packed dirt",10,"PeachPuff4")),2),
                        "stonedirtdirtstone":(copy.deepcopy(Block("dirt stone",15,"salmon4")),2)}