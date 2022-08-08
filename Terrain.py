import random
from Block import *
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([Block("sky",0,"SkyBlue1",False,False)]*self.cols) for row in range(self.rows)]
    
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
        for i in range(self.rows):
            randNum = random.randint(0,10)
            if i == 0:
                self.map[0].insert(0,Block("sky",0,"SkyBlue1",False))
            if i == self.rows-1:
                self.map[0].insert(0,Block("bedrock",1000,"gray4",True,False))
            # else:
                # self.map[i].insert(0,self.map[i][0])
                # print(f"rows: {len(self.map)}\ncols: {len(self.map[0])}")
            if randNum<=4:#stay even
                self.map[i].insert(0,self.map[i][0])
            elif randNum<=7:#increase terrain
                self.map[i].insert(0,self.map[i][0])
                self.map[i-1][0] = self.map[i][0]
            else: #decrease terrain
                self.map[i].insert(0,self.map[i-1][0])
            if i>75 and i<77 and self.map[i][0].solid:
                self.map[i][0] = Block("dirt",10,"tan4")
            if i <75 and self.map[i][0].solid:
                self.map[i][0] = Block("sky",0,"SkyBlue1",False)
                
            
            # else:
            #     x+=1
            #     self.map[i].insert(0,0)
