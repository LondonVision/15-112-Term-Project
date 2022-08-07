import time
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
        start = time.time()
        for visRow in range (self.visRows):
            for visCol in range (self.visCols):
                posRow = self.row + visRow
                posCol = self.col + visCol
                self.visable[visRow][visCol] = app.world.map[(posRow-self.visRows//2)%app.world.cols][(posCol-self.visCols//2)%app.world.cols]
        print(f"time take = {(time.time()-start)*1000//1}")
                        
    def move(self,app,dx):
        # oldCol = int((self.x) / app.cellWidth)        
        # self.x += dx
        self.col += dx
        print(f"moving - {self.col}")
        # newCol = int((self.x) / app.cellWidth)
        # self.col = newCol
        if self.col < 20:
            for i in range(dx):
                app.world.expandMapLeft()
