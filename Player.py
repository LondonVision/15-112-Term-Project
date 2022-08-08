import time
from Block import*
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
        if self.col+len(app.world.map[100]) <= len(app.world.map[0])+20 :
            app.world.expandMapLeft(app)
            self.col += 1000
        if self.col-len(app.world.map[100]) >= -20:
            app.world.expandMapRight(app)
        self.col += dx
        self.refreshPlayerVision(app)
                
    def jump(self,app):
        self.row -= 2
        self.refreshPlayerVision(app)
    
    def mine(self,app,x,y):
        # print("Mining away")
        locRow = (self.row+x-self.visRows//2)
        locCol = (self.col+y-self.visCols//2)
        # print(f"row:{locRow} | col:{locCol}")
        # print(app.world.map[locRow][locCol].tough)
        if app.world.map[locRow][locCol].mineable:
            app.world.map[locRow][locCol].tough -= 1
        if app.world.map[locRow][locCol].tough <= 0:
            for row in range(len(self.inventory)):
                for col in range(len(self.inventory[0])):
                    if self.inventory[row][col] == None:
                        self.inventory[row][col] = app.world.map[locRow][locCol]
            app.world.map[locRow][locCol] = Block("background",0,"gray65",False,False)
        self.refreshPlayerVision(app)            
