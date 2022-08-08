import random,copy
from Block import *
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([Block("sky",1,"SkyBlue1",False,False)]*self.cols) for row in range(self.rows)]
    
    def createLevel(self,heighest,block):
        x = 1000000
        for i in range(heighest,self.rows):
            for j in range(self.cols):
                randNum = random.randint(0,1000000)
                if self.map[i][j] == block:
                    continue
                if randNum >= x:
                    self.map[i][j] = copy.copy(block)
                if (not j == 0) and (not j == self.cols-1) and (not i == 0):
                    if (self.map[i-1][j-1] == block or self.map[i-1][j+1] == block 
                        or self.map[i-1][j] == block):
                        self.map[i][j] = copy.copy(block)
                        if randNum >= x//2:
                            self.map[i-1][j]=copy.copy(block)
                if j == 0 and not i == 0 and self.map[i-1][j+1] == block:
                    self.map[i][j] = copy.copy(block)
                if j == self.cols-1 and not i == 0 and self.map[i-1][j-1] == block:
                    self.map[i][j] = copy.copy(block)
                x -= 1
        
    def createMap(self,L):#list of tuples of information
        for layer,block in L:
            self.createLevel(layer,block)
            
    def createChunk(self,size,L):
        chunk = [([Block("sky",0,"SkyBlue1",False,False)]*size) for row in range(self.rows)]
        for layer,block in L:
            x = 1000000
            for i in range(layer,self.rows):
                for j in range(size):
                    randNum = random.randint(0,1000000)
                    if chunk[i][j] == copy.copy(block):
                        continue
                    if randNum >= x:
                        chunk[i][j] = copy.copy(block)
                    if (not j == 0) and (not j == size-1) and (not i == 0):
                        if (chunk[i-1][j-1] == block or chunk[i-1][j+1] == block 
                            or chunk[i-1][j] == block):
                            chunk[i][j] = copy.copy(block)
                            if randNum >= x//2:
                                chunk[i-1][j]=copy.copy(block)
                    if j == 0 and not i == 0 and chunk[i-1][j+1] == block:
                        chunk[i][j] = copy.copy(block)
                    if j == size-1 and not i == 0 and chunk[i-1][j-1] == block:
                        chunk[i][j] = copy.copy(block)
                    x -= 1
        return chunk
        
    def expandMapLeft(self,app):
        chunk = self.createChunk(1000,app.layers)
        for i in range(self.rows):
            self.insertRow(chunk[i],self.map[i])
            
    def insertRow(self,L1,L2): #It lended itself to recursion :)
        if L1 == []:
            return []
        else:
            L2.insert(0,L1[-1])
            return self.insertRow(L1[:-1],L2)
        
    def expandMapRight(self,app):
        chunk = self.createChunk(1000,app.layers)
        for i in range(self.rows):
            self.map[i].extend(chunk[i])
    