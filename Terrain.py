import random,copy
from Block import *
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([Block("sky",1,"SkyBlue1",False,False)]*self.cols) for row in range(self.rows)]
    
    def createLevel(self,heighest,block,L,size):
        x = 1000000
        for i in range(heighest,self.rows):
            for j in range(size):
                randNum = random.randint(0,1000000)
                if L[i][j] == block:
                    continue
                if randNum >= x:
                    L[i][j] = copy.copy(block)
                if (not j == 0) and (not j == size-1) and (not i == 0):
                    if (L[i-1][j-1] == block or L[i-1][j+1] == block 
                        or L[i-1][j] == block):
                        L[i][j] = copy.copy(block)
                        if randNum >= x//2:
                            L[i-1][j]=copy.copy(block)
                if j == 0 and not i == 0 and L[i-1][j+1] == block:
                    L[i][j] = copy.copy(block)
                if j == size-1 and not i == 0 and L[i-1][j-1] == block:
                    L[i][j] = copy.copy(block)
                x -= 1
        
    def createMap(self,L):#list of tuples of information
        for layer,block in L:
            self.createLevel(layer,block,self.map,self.cols)
        # self.caveGen(self.map, 3)
            
    def caveGen(self,L,passes):
        for row in range(len(L)):
            for col in range(len(L[0])):
                if L[row][col].solid and random.randint(0,5)==5:
                    L[row][col] = Block("background",1,"gray65",False,False)
        print("holes")
        
        possible = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,1),(1,-1)]            
        for i in range(passes):
            for row in range(1,len(L)-1):
                for col in range(1,len(L[0])-1):
                    count = 0
                    for dx,dy in possible:
                        if not L[row+dy][col+dx].solid:
                            count+=1
                    if count >= 6:
                        L[row][col] = Block("background",1,"gray65",False,False)
        print("Cave Gen")
                            
    
    def createChunk(self,size,L):
        chunk = [([Block("sky",0,"SkyBlue1",False,False)]*size) for row in range(self.rows)]
        for layer,block in L:
            self.createLevel(layer, block, chunk, size)
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