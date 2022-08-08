
class Block(object):
    def __init__(self,name,tough,color,solid=True,mineable=True):
        self.name = name
        self.tough = tough
        self.color = color
        self.solid = solid
        self.mineable = mineable
    
    def __eq__(self,other):
        if isinstance(other,Block) and self.name == other.name:
            return True
        return False