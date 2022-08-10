
class Block(object):
    def __init__(self,name,tough,color,solid=True,mineable=True):
        self.name = name
        self.tough = tough
        self.color = color
        self.solid = solid
        self.mineable = mineable
        self.drops = self
    
    def __eq__(self,other):
        if isinstance(other,Block) and self.name == other.name:
            return True
        return False
    
    def __repr__(self):
        return f"Name: {self.name}"

class Ore(Block):
    def __init__(self,name,tough,color):
        super().__init__(name, tough, color)