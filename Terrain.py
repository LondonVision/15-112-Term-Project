import random,copy
from Block import *
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([Block("sky",1,"SkyBlue1",False,False)]*self.cols) for row in range(self.rows)]
        self.text = ""
        
    def createLevel(self,heighest,block,L,size):
        x = 1000000
        self.text = f"Creating {block.name} layer"
        print(self.text)
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
        
    def createMap(self,L,J):#L = list of tuples of information
        for layer,block in L:
            self.createLevel(layer,block,self.map,self.cols)
        self.caveGen(self.map, 10) #increasing this number increases the "smoothness" of caves
        self.sprinkle(self.map,J)
        for col in range(len(self.map[0])):
            self.map[len(self.map)-1][col] = Block("bedrock",1000,"gray4",True,False)
            
    def caveGen(self,L,passes): #example 7 - https://www.cs.cmu.edu/~112/notes/student-tp-guides/Terrain.pdf
        for row in range(80,len(L)-1): #80 because highest dirt is 75 and some top layer should be preserved
            for col in range(len(L[0])):
                if L[row][col].solid and random.randint(0,100)<=37: #hole randomness
                    L[row][col] = Block("background",1,"gray65",False,False)
        self.text= "Generating Caves..."
        print(self.text)
        #I used a set for its attribute of being unordered and cause its fast
        possible = set([(1,0),(1,1),(1,-1),(0,-1),(0,1),(-1,0),(-1,-1),(-1,1)])          
        for i in range(passes):
            self.text = f"Smoothing Caves: {(i+1)*10}%"
            print(self.text)
            for row in range(80,len(L)-1):
                for col in range(1,len(L[0])-1):
                    air = 0
                    for drow,dcol in possible:
                        if (not L[row+drow][col+dcol].solid and 
                            not L[row+drow][col+dcol].name == "sky"):
                            air+=1
                    if air >= 5: #if there are x air blocks around this block, it is air
                        L[row][col] = Block("background",1,"gray65",False,False)
                    if air <= 2: #if there are less than x air blocks around this block, it is solid
                        for drow,dcol in possible:
                            if (L[row+drow][col+dcol].solid and 
                                not L[row][col].name == "sky"):
                                L[row][col] = copy.deepcopy(L[row+drow][col+dcol])
                                break
        self.text = "Cave Gen complete"
        print(self.text)
            
    def createOre(self,top,bottom,ore,L,size):
        self.text = f"Sprinkling in {ore.name}"
        print(self.text)
        for row in range(top,bottom):
            for col in range(1,size-1):
                possible = [(1,0),(1,1),(1,-1),(0,-1),(0,1),(-1,0),(-1,-1),(-1,1)]
                random.shuffle(possible)
                score = 0
                for drow,dcol in possible:
                    if (isinstance(L[row+drow][col+dcol],Ore) or 
                        not L[row+drow][col+dcol].solid):
                        score+=1
                randNum = random.randint(0,100)
                if score == 0 and randNum<2:
                    L[row][col] = copy.deepcopy(ore)
                    for drow,dcol in possible:
                        if L[row+drow][col+dcol].solid:
                            L[row+drow][col+dcol] = copy.deepcopy(ore)
                            randNum -= 1
                        if randNum <= 0:
                            break
                        
    def sprinkle(self,L,J):
        for top,bottom,ore in J:
            self.createOre(top,bottom,ore,L,len(L[0]))
                
    def createChunk(self,size,L,J):
        chunk = [([Block("sky",0,"SkyBlue1",False,False)]*size) for row in range(self.rows)]
        for layer,block in L:
            self.createLevel(layer, block, chunk, size)
        self.caveGen(chunk, 10)
        self.sprinkle(chunk,J)
        for col in range(len(chunk[0])):
            self.map[len(chunk)-1][col] = Block("bedrock",1000,"gray4",True,False)
        return chunk
        
    def expandMapLeft(self,app):
        chunk = self.createChunk(100,app.layers,app.ores)
        for i in range(self.rows):
            self.insertRow(chunk[i],self.map[i])
            
    def insertRow(self,L1,L2): #It lended itself to recursion :)
        if L1 == []:
            return []
        else:
            L2.insert(0,L1[-1])
            return self.insertRow(L1[:-1],L2)
        
    def expandMapRight(self,app):
        chunk = self.createChunk(100,app.layers,app.ores)
        for i in range(self.rows):
            self.map[i].extend(chunk[i])