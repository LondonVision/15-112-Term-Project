
class Player(object):
    def __init__(self,app):
        self.health = 20
        self.x = app.width/2
        self.y = app.height/2
        self.col = app.cols//2
        self.row = app.rows//2
        self.visCols = 40
        self.visRows = 40
        self.visable = [([0]*self.visCols) for row in range(self.visRows)]
        
    def refreshPlayerVision(self,app):
        for visRow in range (40):
            for visCol in range (40):
                posRow = self.row + visRow
                posCol = self.col + visCol
                self.visable[visRow][visCol] = app.map[posRow-20][posCol-20]
                        
    def move(self,app,dx):
        # oldCol = int((self.x) / app.cellWidth)        
        # self.x += dx
        self.col += dx
        # newCol = int((self.x) / app.cellWidth)
        # self.col = newCol
