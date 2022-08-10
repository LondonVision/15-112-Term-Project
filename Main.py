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
    app.blockToughDict = {"dirt":5,"stone":10,"deep stone":20}
    app.world = Terrain(app,app.rows,app.cols)
    app.world.createMap(app.layers)
    print("Game Launching...")
    app.player = Player(app)
    app.player.refreshPlayerVision(app)
    app.invOpen = False
    
    app.cellWidth = app.width / app.player.visCols
    app.timerDelay = 98
    
    app.mouseX = 0
    app.mouseY = 0
                  
def timerFired(app):
    if not app.world.map[app.player.row+1][app.player.col].solid:
        app.player.row+=1
        app.player.refreshPlayerVision(app)
                                
def keyPressed(app, event):
    if (event.key == "a"):
        app.player.move(app,-1)
    if (event.key == "d"): 
        app.player.move(app,+1)
    if (event.key == "Space"):
        app.player.jump(app)
    if (event.key == "e"):
        app.invOpen = not app.invOpen
    if (event.key in set(["1","2","3","4","5","6","7","8","9","0"])):
        if event.key == "0":
            app.player.hotbarSlot = 9
        else:
            app.player.hotbarSlot = int(event.key)-1

def mouseMoved(app,event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app,event):
    row,col = getCell(app,event.x,event.y)
    miniRow,miniCol = int((event.y) / app.cellWidth/2),int((event.x) / app.cellWidth/2)
    #player can only mine in a 5x5 grid around themselves
    if (app.invOpen and miniRow >= 0 and miniRow < len(app.player.inventory) and
        miniCol >=0 and miniCol < len(app.player.inventory[0])):
        if app.player.selected == None:
            print("trying")
            app.player.selected = app.player.inventory[miniRow][miniCol]
            app.player.inventory[miniRow][miniCol] = None
        elif (not app.player.selected == None and 
            app.player.inventory[miniRow][miniCol] == None):
            app.player.inventory[miniRow][miniCol] = app.player.selected
            app.player.selected = None
        print(f"row: {miniRow} col: {miniCol}")
        print(app.player.selected)
    
    if (row>app.player.visRows//4 and row<app.player.visRows*3//4 and
        col>app.player.visRows//4 and col<app.player.visCols*3//4):
        if (not isinstance(app.player.inventory[0][app.player.hotbarSlot],tuple) or
            app.player.inventory[0][app.player.hotbarSlot] == None):
            app.player.mine(app,row,col)
        else:
            app.player.placeBlock(app,row,col)
   
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
            
def redrawAll(app,canvas):
    app.player.redraw(app,canvas)

runApp(width=600, height=600)