import random
from Block import *
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([Block("sky",0,"light blue",False)]*self.cols) for row in range(self.rows)]
    
    def createLevel(self,heighest,block):
        x = 1000000
        for i in range(heighest,self.rows):
            for j in range(self.cols):
                randNum = random.randint(0,1000000)
                if self.map[i][j] == block:
                    continue
                if randNum >= x:
                    self.map[i][j] = block
                if (not j == 0) and (not j == self.cols-1) and (not i == 0):
                    if (self.map[i-1][j-1] == block or self.map[i-1][j+1] == block 
                        or self.map[i-1][j] == block):
                        self.map[i][j] = block
                        if randNum >= x//2:
                            self.map[i-1][j]=block
                if j == 0 and not i == 0 and self.map[i-1][j+1] == block:
                    self.map[i][j] = block
                if j == self.cols-1 and not i == 0 and self.map[i-1][j-1] == block:
                    self.map[i][j] = block
                x -= 1
        
    def createMap(self,L):#list of tuples of information
        for layer,block in L:
            self.createLevel(layer,block)
            
        
        
        
    def expandMapLeft(self):
        print("expanding map")
        randNum = random.randint(0,1000000)
        x=0
        for i in range(len(self.rows)):
            if i == 0:
                self.map[0].insert(0,0)
            elif self.map[i-1][0] == 1:
                self.map[i].insert(0,1)
            elif self.map[i][0] == 1:
                if randNum<=500000:
                    self.map[i].insert(0,1)
                elif randNum<750000:
                    self.map[i].insert(0,1)
                    self.map[i+1][0] = 1
                else:
                    self.map[i].insert(0,0)
            else:
                x+=1
                self.map[i].insert(0,0)
        print(x)