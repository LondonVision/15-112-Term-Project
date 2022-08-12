from cmu_112_graphics import *
from Player import *
from Terrain import *
from Block import *
from Craft import *
import random,sys

def appStarted(app):
    sys.setrecursionlimit(1500) #https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
    app.rows = 200
    app.cols = 1000 #!1000
    
    app.layers = [(75,Block("dirt",5,"tan4")),
              (85,Block("stone",10,"light slate gray")),
              (125,Block("deep stone",20,"gray20")),
              (180,Block("bedrock",1000,"gray4",True,False))]
    app.ores = [(90,120,Ore("iron ore",15,"MistyRose2")),
                (120,150,Ore("gold ore",20,"goldenrod4")),
                (150,180,Ore("diamond ore",25,"DodgerBlue4"))]
    app.blockToughDict = {"dirt":5,"stone":10,"deep stone":20,
                          "iron ore":15,"gold ore":20,"diamond ore":25,
                          "packed dirt":10,"dirt stone":15,
                          "iron":20,"gold":10,"diamond":25}
    app.world = Terrain(app,app.rows,app.cols)
    app.world.createMap(app.layers,app.ores)
    app.world.text = "Game Launching..."
    print("Game Launching...")
    app.player = Player(app)
    app.player.refreshPlayerVision(app)
    app.invOpen = False
    app.cellWidth = app.width / app.player.visCols
    app.timerDelay = 98
    
    app.craft = Craft()
    
    app.mouseX = 0
    app.mouseY = 0
                  
def timerFired(app):
    if not app.world.map[app.player.row+1][app.player.col].solid:
        app.player.row+=1
        app.player.refreshPlayerVision(app)
    if app.invOpen:
        checkCraftingGrid(app)
                                
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
    row,col = int((app.mouseY) / app.cellWidth/2),int((app.mouseX) / app.cellWidth/2)
    if (event.key == "x" and app.player.selected == None and
        row <= len(app.player.inventory) and col <= len(app.player.inventory[0]) and
        isinstance(app.player.inventory[row][col],tuple) and app.player.inventory[row][col][1]>1):
        block,amount = app.player.inventory[row][col]
        newAmount = amount//2
        amount -= newAmount
        app.player.inventory[row][col] = (block,amount)
        app.player.selected = (block,newAmount)        

def mouseMoved(app,event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app,event):
    row,col = getCell(app,event.x,event.y)
    miniRow,miniCol = int((event.y) / app.cellWidth/2),int((event.x) / app.cellWidth/2)
    #player can only mine in a 5x5 grid around themselves
    #moving items in inventory
    if (app.invOpen and miniRow >= 0 and miniRow < len(app.player.inventory) and
        miniCol >=0 and miniCol < len(app.player.inventory[0])):
        moveItem(app,app.player.inventory,miniRow,miniCol)
    #moving items around crafting grid
    if (app.invOpen and miniRow >= 1 and miniRow <= 2 and miniCol >= 11 and miniCol <=13):
        moveItem(app,app.player.craftingGrid,miniRow-1,miniCol-11)  
        checkCraftingGrid(app)
    if (app.invOpen and miniRow == 1 and miniCol == 14 and 
        not app.player.output == None):
        app.player.selected = app.player.output
        app.player.output = None
        for row in range (len(app.player.craftingGrid)):
            for col in range(len(app.player.craftingGrid[0])):
                if not app.player.craftingGrid[row][col]==None:
                    block,amount = app.player.craftingGrid[row][col]
                    amount -= 1
                    if amount <= 0:
                        app.player.craftingGrid[row][col] = None
                    else:
                        app.player.craftingGrid[row][col] = (block,amount)
    #mining and building
    if (row>app.player.visRows//4 and row<app.player.visRows*3//4 and
        col>app.player.visRows//4 and col<app.player.visCols*3//4):
        if (not isinstance(app.player.inventory[0][app.player.hotbarSlot],tuple) or
            app.player.inventory[0][app.player.hotbarSlot] == None):
            app.player.mine(app,row,col)
        else:
            app.player.placeBlock(app,row,col)
    
def moveItem(app,L,row,col):
    if app.player.selected == None:
        app.player.selected = L[row][col]
        L[row][col] = None
    elif (not app.player.selected == None and 
        L[row][col] == None):
        L[row][col] = app.player.selected
        app.player.selected = None
    elif (not app.player.selected == None and not L[row][col] == None
          and app.player.selected[0]==L[row][col][0]):
        L[row][col] = (app.player.selected[0],
                                             app.player.selected[1]+L[row][col][1])
        app.player.selected = None

#I used this for the idea to turn the grid into a string
#https://gamedev.stackexchange.com/questions/21586/how-could-i-implement-something-like-minecrafts-crafting-grid#:~:text=The%20crafting%20system%20in%20Minecraft,exchange%20certain%20ingredients%20for%20others.
def checkCraftingGrid(app):
    result = ""
    for row in range(len(app.player.craftingGrid)):
        for col in range(len(app.player.craftingGrid[0])):
            if app.player.craftingGrid[row][col]==None:
                result += "None"
            else:
                result += app.player.craftingGrid[row][col][0].name
    if result in app.craft.recipes:
        app.player.output = app.craft.recipes[result]
    else:
        app.player.output = None

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