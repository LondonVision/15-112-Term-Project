from cmu_112_graphics import *
from Player import *
from Terrain import *
from Block import *
import random

def appStarted(app):
    app.rows = 200
    app.cols = 1000
    
    layers = [(75,Block("dirt",10,"tan4")),
              (85,Block("stone",20,"light slate gray")),
              (125,Block("deep stone",30,"gray20")),
              (180,Block("bedrock",1000,"gray4",True,False))]
    app.world = Terrain(app,app.rows,app.cols)
    app.world.createMap(layers)
    
    app.player = Player(app)
    app.player.refreshPlayerVision(app)
    app.cellWidth = app.width / app.player.visCols
    
    # app.timerDelay = 2
                    
    
def keyPressed(app, event):
    if (event.key == "a"):
        app.player.move(app,-10)
    elif (event.key == "d"): 
        app.player.move(app,+10)
    if (event.key == "Space"):
        app.player.jump(app)
    if (event.key == "Down"): #TODO this is temperary - gravity will do this
        app.player.row += 1
        app.player.refreshPlayerVision(app)

def mousePressed(app,event):
    row,col = getCell(app,event.x,event.y)
    if (row>app.player.visRows//4 and row<app.player.visRows*3//4 and
        col>app.player.visRows//4 and col<app.player.visCols*3//4):
        app.player.mine(app,row,col)

def timerFired(app):
    # app.player.refreshPlayerVision(app)
    pass
     
def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    row = int((y) / app.cellWidth)
    col = int((x) / app.cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = col * app.cellWidth
    x1 = (col+1) * app.cellWidth
    y0 = row * app.cellWidth
    y1 = (row+1) * app.cellWidth
    return (x0, y0, x1, y1)

def drawVisable(app,canvas):
    for row in range(len(app.player.visable)):
        for col in range(len(app.player.visable[0])):
            color = app.player.visable[row][col].color
            x0,y0,x1,y1 = getCellBounds(app,row,col)
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)

def drawPlayer(app,canvas):
    # w = app.cellWidth/2
    # canvas.create_rectangle(app.player.x-w,app.player.y-w,
                            # app.player.x+w,app.player.y+w,fill="red")
    x0,y0,x1,y1 = getCellBounds(app,20,20)
    canvas.create_rectangle(x0,y0,x1,y1,fill="red")
    
def drawCoords(app,canvas):
    canvas.create_text(app.width/2,0,
                       text=f"x: {app.player.col}\ny: {app.player.row}",
                       anchor="n")

def redrawAll(app,canvas):
    drawVisable(app,canvas)
    drawPlayer(app,canvas)
    drawCoords(app,canvas)

runApp(width=600, height=600)