
class Block(object):
    def __init__(self,name,tough,color,solid=True):
        self.name = name
        self.tough = tough
        self.color = color
        self.solid = solid
    
    def __eq__(self,other):
        if isinstance(other,Block) and self.name == other.name:
            return True
        return False