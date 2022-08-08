import time
class Player(object):
    def __init__(self,app):
        self.health = 20
        self.inventory = [([None]*4) for row in range(9)]
        self.x = app.width/2
        self.y = app.height/2
        self.col = app.cols//2
        self.row = app.rows//2
        x = 0
        while not self.isPositionLegal(app):
            self.row = app.rows-1-x
            x+=1
        self.visCols = 40
        self.visRows = 40
        self.visable = [([0]*self.visCols) for row in range(self.visRows)]
        
    def refreshPlayerVision(self,app):
        start = time.time()
        for visRow in range (self.visRows):
            for visCol in range (self.visCols):
                posRow = self.row + visRow
                posCol = self.col + visCol
                self.visable[visRow][visCol] = (app.world.map[(posRow-self.visRows//2)]
                                                [(posCol-self.visCols//2)])
        print(f"time take = {(time.time()-start)*1000//1}")
    
    def isPositionLegal(self,app):
        if app.world.map[self.row][self.col].solid:
            return False
        return True 
    
    def move(self,app,dx):
        # oldCol = int((self.x) / app.cellWidth)        
        # self.x += dx
        
        # newCol = int((self.x) / app.cellWidth)
        # self.col = newCol
        if self.col+len(app.world.map[0]) <= len(app.world.map[0])+20 :
            for i in range(100):
                app.world.expandMapLeft()
            self.col += 100
        self.col += dx
        self.refreshPlayerVision(app)
                
    def jump(self,app):
        self.row -= 2
        self.refreshPlayerVision(app)
