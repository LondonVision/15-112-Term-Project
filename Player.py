import time,copy
from Block import*
from cmu_112_graphics import *
class Player(object):
    def __init__(self,app):
        self.health = 20
        self.inventory = [([None]*10) for row in range(4)]
        self.hotbarSlot = 0
        self.selected = None
        
        self.craftingGrid = [([None]*2) for i in range(2)]
        self.output = None
        
        self.visCols = 40
        self.visRows = 40
        
        self.col = app.cols//2
        self.row = self.visRows
        while not app.world.map[self.row+1][self.col].solid:
            self.row += 1
    
        self.visable = [([0]*self.visCols) for row in range(self.visRows)]
        
        self.playerSprite = app.loadImage('playerSprite.png')
        self.playerSprite = app.scaleImage(self.playerSprite,1/44)

        
    def refreshPlayerVision(self,app):
        if self.row + self.visRows//2 >= len(app.world.map):
            var = self.visRows//2+(len(app.world.map)-self.row)
            for visRow in range (var):
                for visCol in range (self.visCols):
                    posRow = self.row + visRow - self.visRows//2
                    posCol = self.col + visCol - self.visCols//2
                    self.visable[visRow][visCol] = app.world.map[posRow][posCol]
            for newrow in range (var,self.visRows):
                for newcol in range (self.visCols):
                    self.visable[newrow][newcol] = Block("bedrock",1000,"gray4",True,False)
        elif self.row - self.visRows//2 <= 0:
            var = self.visRows//2-(self.row)
            for visRow in range (var,self.visRows):
                for visCol in range (self.visCols):
                    posRow = self.row + visRow - self.visRows//2
                    posCol = self.col + visCol - self.visCols//2
                    self.visable[visRow][visCol] = app.world.map[posRow][posCol]
            for newrow in range (var):
                for newcol in range (self.visCols):
                    self.visable[newrow][newcol] = Block("sky",0,"SkyBlue1",False,False)
        else:        
            for visRow in range (self.visRows):
                for visCol in range (self.visCols):
                    posRow = self.row + visRow - self.visRows//2
                    posCol = self.col + visCol - self.visCols//2
                    self.visable[visRow][visCol] = app.world.map[posRow][posCol]
            
    def isPositionLegal(self,app):
        if app.world.map[self.row][self.col].solid:
            return False
        return True 
    
    def move(self,app,dx):
        if self.col <= self.visCols//2:
            app.world.expandMapLeft(app)
            self.col += 100
        if self.col-len(app.world.map[0]) >= -20:
            app.world.expandMapRight(app)
        
        self.col += dx
        if not self.isPositionLegal(app):
            self.col -= dx
        if not app.world.map[self.row+1][self.col].solid:
            self.row += 1
        self.refreshPlayerVision(app)
                
    def jump(self,app):
        if app.world.map[self.row+1][self.col].solid:
            self.row -= 2
        if not self.isPositionLegal(app):
            self.row += 2
        self.refreshPlayerVision(app)
    
    def addBlockToInventory(self,item):
        breakFlag = False
        for row in range(len(self.inventory)):
            for col in range(len(self.inventory[0])):
                if isinstance(self.inventory[row][col],tuple) and item in self.inventory[row][col]:
                    block,amount = self.inventory[row][col]
                    self.inventory[row][col] = (block,amount+1)
                    breakFlag = True
                    break
                elif self.inventory[row][col] == None:
                    self.inventory[row][col] = (item,1)
                    breakFlag = True
                    break
            if breakFlag:
                break
            
    def mine(self,app,x,y):
        # print("Mining away")
        locRow = (self.row+x-self.visRows//2)
        locCol = (self.col+y-self.visCols//2)
        # print(f"row:{locRow} | col:{locCol}")
        # print(app.world.map[locRow][locCol].tough)
        if app.world.map[locRow][locCol].mineable:
            app.world.map[locRow][locCol].tough -= 1 #!this should be 1
            if app.world.map[locRow][locCol].tough <= 0:
                temp = app.world.map[locRow][locCol].drops
                temp.tough = app.blockToughDict.get(temp.name)
                self.addBlockToInventory(copy.deepcopy(temp))
                if locRow<90:
                    app.world.map[locRow][locCol] = Block("sky",0,"SkyBlue1",False,False)
                else:
                    app.world.map[locRow][locCol] = Block("background",1,"gray65",False,False)
        self.refreshPlayerVision(app)
    
    def placeBlock(self,app,row,col):
        locRow = (self.row+row-self.visRows//2)
        locCol = (self.col+col-self.visCols//2)
        if not isinstance(self.inventory[0][self.hotbarSlot],tuple): #if its not a block,don't place it
            return
        elif self.inventory[0][self.hotbarSlot] == None: #if the slot is empty, don't do anything
            return
        elif app.world.map[locRow][locCol].solid: #if the location is not valid, don't place it
            return
        block,amount = self.inventory[0][self.hotbarSlot]
        app.world.map[locRow][locCol] = copy.deepcopy(block)
        amount-=1
        if amount <= 0:
            self.inventory[0][self.hotbarSlot] = None
        else:
            self.inventory[0][self.hotbarSlot] = (block,amount)
        self.refreshPlayerVision(app)

    def drawVisable(self,app,canvas):
        for row in range(len(self.visable)):
            for col in range(len(self.visable[0])):
                color = self.visable[row][col].color
                outline = color
                x0,y0,x1,y1 = self.getCellBounds(app,row,col,app.cellWidth)
                canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline=outline)

    def drawPlayer(self,app,canvas):
        # w = app.cellWidth/2
        # canvas.create_rectangle(app.player.x-w,app.player.y-w,
                                # app.player.x+w,app.player.y+w,fill="red")
        x0,y0,x1,y1 = self.getCellBounds(app,20,20,app.cellWidth)
        canvas.create_image((x0+x1)/2,(y0+y1)/2,image=ImageTk.PhotoImage(self.playerSprite))
        
    def drawCoords(self,app,canvas):
        canvas.create_text(app.width/2,0,
                        text=f"x: {self.col}\ny: {self.row}",
                        anchor="n")

    def drawInventory(self,app,canvas):
        for row in range(len(self.inventory)):
            for col in range(len(self.inventory[0])):
                block,amount = None,0
                if isinstance(self.inventory[row][col],tuple):
                    block,amount = self.inventory[row][col]
                color = "LightBlue3"
                if not block == None:
                    color = block.color
                if amount == 0:
                    amount = ""
                x0,y0,x1,y1 = self.getCellBounds(app,row,col,app.cellWidth*2)
                canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue3")
                canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=color,outline=color)
                canvas.create_text((x0+x1)/2,(y0+y1)/2,text=amount)
                
    def drawHotbar(self,app,canvas):
        for col in range(len(self.inventory[0])):
            block,amount = None,0
            if isinstance(self.inventory[0][col],tuple):
                block,amount = self.inventory[0][col]
            color = "LightBlue3"
            if not block == None:
                color = block.color
            if amount == 0:
                amount = ""
            x0 = col*(app.width/12.5) + app.width/10
            x1 = (col+1)*(app.width/12.5) + app.width/10
            y0 = app.height*16.5/20
            y1 = app.height*18.1/20
            canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue3")
            canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=color,outline=color)
            canvas.create_text((x0+x1)/2,(y0+y1)/2,text=amount)
            
    def drawHotbarSelected(self,app,canvas):
        x0 = self.hotbarSlot*(app.width/12.5) + app.width/10
        x1 = (self.hotbarSlot+1)*(app.width/12.5) + app.width/10
        y0 = app.height*16.5/20
        y1 = app.height*18.1/20
        canvas.create_line(x0,y0,x1,y0,fill="snow",width="3")
        canvas.create_line(x0,y1,x1,y1,fill="snow",width="3")
        canvas.create_line(x0,y0,x0,y1,fill="snow",width="3")
        canvas.create_line(x1,y1,x1,y0,fill="snow",width="3")
    
    def drawSelected(self,app,canvas):
        if isinstance(self.selected,tuple):
                block,amount = self.selected
        canvas.create_rectangle(app.mouseX-app.cellWidth+4, app.mouseY-app.cellWidth+4,
                                app.mouseX+app.cellWidth-4, app.mouseY+app.cellWidth-4,
                                fill=block.color)
        canvas.create_text(app.mouseX,app.mouseY,text=amount)
    
    def drawCraftingGrid(self,app,canvas):
        for row in range(len(self.craftingGrid)):
            for col in range(len(self.craftingGrid[0])):
                block,amount = None,0
                if isinstance(self.craftingGrid[row][col],tuple):
                    block,amount = self.craftingGrid[row][col]
                color = "LightBlue3"
                if not block == None:
                    color = block.color
                if amount == 0:
                    amount = ""
                x0,y0,x1,y1 = self.getCellBounds(app,row+1,col+11,app.cellWidth*2)
                canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue3")
                canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=color,outline=color)
                canvas.create_text((x0+x1)/2,(y0+y1)/2,text=amount)
                
    def drawOutput(self,app,canvas):
        block,amount = None,0
        if isinstance(self.output,tuple):
            block,amount = self.output  
        color = "LightBlue3"
        if not block == None:  
            color = block.color
        if amount == 0:
            amount = ""
        x0,y0,x1,y1 = self.getCellBounds(app,1,14,app.cellWidth*2)
        canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue3")
        canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=color,outline=color)
        canvas.create_text((x0+x1)/2,(y0+y1)/2,text=amount)
        
    def getCellBounds(self,app, row, col,width): #same link as above
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 = col * width
        x1 = (col+1) * width
        y0 = row * width
        y1 = (row+1) * width
        return (x0, y0, x1, y1)
    
    def redraw(self,app,canvas):
        self.drawVisable(app,canvas)
        self.drawPlayer(app,canvas)
        self.drawCoords(app,canvas)
        self.drawHotbar(app,canvas)
        self.drawHotbarSelected(app,canvas)
        if app.invOpen:
            self.drawInventory(app,canvas)
            self.drawCraftingGrid(app, canvas)
            self.drawOutput(app, canvas)
            if not self.selected == None:
                self.drawSelected(app, canvas)