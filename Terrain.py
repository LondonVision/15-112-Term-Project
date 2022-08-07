import random
class Terrain(object):
    def __init__(self,app,rows,cols):
        self.rows = rows
        self.cols = cols
        self.map = [([0]*self.cols) for row in range(self.rows)]
    
    def createMap(self):
        x = 1000000
        for i in range(75,self.rows):
            for j in range(self.cols):
                randNum = random.randint(0,1000000)
                if self.map[i][j] == 1:
                    continue
                if randNum >= x:
                    self.map[i][j] = 1
                if (not j == 0) and (not j == self.cols-1) and (not i == 0):
                    if (self.map[i-1][j-1] == 1 or self.map[i-1][j+1] == 1 
                        or self.map[i-1][j] == 1):
                        self.map[i][j] = 1
                        if randNum >= x//2:
                            self.map[i-1][j]=1
                if j == 0 and not i == 0 and self.map[i-1][j+1] == 1:
                    self.map[i][j] = 1
                if j == self.cols-1 and not i == 0 and self.map[i-1][j-1] == 1:
                    self.map[i][j] = 1
                x -= 1
        self.map[101][0] = 0
        
    def expandMapLeft(self):
        print("expanding map")
        randNum = random.randint(0,1000000)
        x=0
        for i in range(len(self.map)):
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