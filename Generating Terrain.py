from cmu_112_graphics import *
import random
def appStarted(app):
    app.rows = 200
    app.cols = 1000
    createMap(app)
    app.playerCx = app.width/2
    app.playerCy = app.height/2
    app.playerRow = app.rows//4
    app.playerCol = app.cols//2

    app.visCols = 40
    app.visRows = 40
    app.visable = [([0]*app.visCols) for row in range(app.visRows)]
    playerVision(app)

    
def createMap(app):
    app.map = [([0]*app.cols) for row in range(app.rows)]
    x = 1000000
    for i in range(50,app.rows):
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
def playerVision(app):
    for visRow in range (40):
        for visCol in range (40):
            posRow = app.playerRow + visRow
            posCol = app.playerCol + visCol
            app.visable[visRow][visCol] = app.map[posRow-20][posCol-20]
    for row in app.visable:
        print(row)

def timerFired(app):
    pass
def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    
    gridWidth  = app.width 
    gridHeight = app.height
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth = gridWidth / app.visCols
    cellHeight = gridHeight / app.visRows
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawVisable(app,canvas):
    for row in range(len(app.visable)):
        for col in range(len(app.visable[0])):
            color = "gray" if app.visable[row][col] == 1 else "blue"
            x0,y0,x1,y1 = getCellBounds(app,row,col)
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)

def redrawAll(app,canvas):
    drawVisable(app,canvas)

runApp(width=600, height=600)