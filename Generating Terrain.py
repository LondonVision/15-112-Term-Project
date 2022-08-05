from cmu_112_graphics import *
from Player import *
import random
def appStarted(app):
    app.rows = 200
    app.cols = 1000
    createMap(app)
    
    app.player = Player(app)
    app.player.refreshPlayerVision(app)
    app.cellWidth = app.width / app.player.visCols
    
    app.left = False
    app.right = False
    app.timerDelay = 2
    
    
def createMap(app):
    app.map = [([0]*app.cols) for row in range(app.rows)]
    x = 1000000
    for i in range(75,app.rows):
        for j in range(app.cols):
            randNum = random.randint(0,1000000)
            if app.map[i][j] == 1:
                continue
            
            if randNum >= x:
                app.map[i][j] = 1
            if (not j == 0) and (not j == app.cols-1) and (not i == 0):
                if (app.map[i-1][j-1] == 1 or app.map[i-1][j+1] == 1 
                    or app.map[i-1][j] == 1):
                    app.map[i][j] = 1
                    if randNum >= x//2:
                        app.map[i-1][j]=1
            if j == 0 and not i == 0 and app.map[i-1][j+1] == 1:
                app.map[i][j] = 1
            if j == app.cols-1 and not i == 0 and app.map[i-1][j-1] == 1:
                app.map[i][j] = 1
            x -= 1

    
def keyPressed(app, event):
    if (event.key == "a"):
        # app.left = True
        app.player.move(app,-1)
    elif (event.key == "d"): 
        # app.right = True
        app.player.move(app,+1)
    app.player.refreshPlayerVision(app)
        
# def keyReleased(app, event):
#     if (event.key == "a"):
#         app.left = False
#     elif (event.key == "d"): 
#         app.right = False
        
def timerFired(app):
    app.player.refreshPlayerVision(app)
#     if app.left:
#         app.player.move(app,-1)
#     elif app.right:
#         app.player.move(app,1)
        
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
            color = "gray" if app.player.visable[row][col] == 1 else "blue"
            x0,y0,x1,y1 = getCellBounds(app,row,col)
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)

def drawPlayer(app,canvas):
    # w = app.cellWidth/2
    # canvas.create_rectangle(app.player.x-w,app.player.y-w,
                            # app.player.x+w,app.player.y+w,fill="red")
    x0,y0,x1,y1 = getCellBounds(app,20,20)
    canvas.create_rectangle(x0,y0,x1,y1,fill="red")
    
    
def redrawAll(app,canvas):
    drawVisable(app,canvas)
    drawPlayer(app,canvas)

runApp(width=600, height=600)