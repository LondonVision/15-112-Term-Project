from cmu_112_graphics import *
from Player import *
from Terrain import *
from Block import *
import random,sys

def appStarted(app):
    sys.setrecursionlimit(1500) #https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
    app.rows = 200
    app.cols = 1000
    
    app.layers = [(75,Block("dirt",5,"tan4")),
              (85,Block("stone",10,"light slate gray")),
              (125,Block("deep stone",20,"gray20")),
              (180,Block("bedrock",1000,"gray4",True,False))]
    app.world = Terrain(app,app.rows,app.cols)
    app.world.createMap(app.layers)
    
    app.player = Player(app)
    app.player.refreshPlayerVision(app)
    app.invOpen = False
    
    app.cellWidth = app.width / app.player.visCols
                        
    
def keyPressed(app, event):
    if (event.key == "a"):
        app.player.move(app,-1)
    if (event.key == "d"): 
        app.player.move(app,+1)
    if (event.key == "Space"):
        app.player.jump(app)
    if (event.key == "Down"): #TODO this is temperary - gravity will do this
        app.player.row += 1
        app.player.refreshPlayerVision(app)
    if (event.key == "e"):
        app.invOpen = not app.invOpen
    

def mousePressed(app,event):
    row,col = getCell(app,event.x,event.y)
    if (row>app.player.visRows//4 and row<app.player.visRows*3//4 and
        col>app.player.visRows//4 and col<app.player.visCols*3//4):
        app.player.mine(app,row,col)

def timerFired(app):
    # app.player.refreshPlayerVision(app)
    pass
     
def getCell(app, x, y): #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    row = int((y) / app.cellWidth)
    col = int((x) / app.cellWidth)
    return (row, col)

def getCellBounds(app, row, col,width): #same link as above
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = col * width
    x1 = (col+1) * width
    y0 = row * width
    y1 = (row+1) * width
    return (x0, y0, x1, y1)

def drawVisable(app,canvas):
    for row in range(len(app.player.visable)):
        for col in range(len(app.player.visable[0])):
            color = app.player.visable[row][col].color
            x0,y0,x1,y1 = getCellBounds(app,row,col,app.cellWidth)
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)

def drawPlayer(app,canvas):
    # w = app.cellWidth/2
    # canvas.create_rectangle(app.player.x-w,app.player.y-w,
                            # app.player.x+w,app.player.y+w,fill="red")
    x0,y0,x1,y1 = getCellBounds(app,20,20,app.cellWidth)
    canvas.create_rectangle(x0,y0,x1,y1,fill="red")
    
def drawCoords(app,canvas):
    canvas.create_text(app.width/2,0,
                       text=f"x: {app.player.col}\ny: {app.player.row}",
                       anchor="n")

def drawInventory(app,canvas):
    for row in range(len(app.player.inventory)):
        for col in range(len(app.player.inventory[0])):
            (block,amount) = app.player.inventory[row][col]
            color = "LightBlue3"
            if not block == None:
                color = block.color
            if amount == 0:
                amount = ""
            x0,y0,x1,y1 = getCellBounds(app,row,col,app.cellWidth*2)
            canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue3")
            canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=color,outline=color)
            canvas.create_text((x0+x1)/2,(y0+y1)/2,text=amount)
            
def redrawAll(app,canvas):
    drawVisable(app,canvas)
    drawPlayer(app,canvas)
    drawCoords(app,canvas)
    if app.invOpen:
        drawInventory(app,canvas)

runApp(width=600, height=600)