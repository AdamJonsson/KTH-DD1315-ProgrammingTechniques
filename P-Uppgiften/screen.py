from tkinter import *
import random
import math
import time

class Screen:
    """
        The tkinter window and the canvas. Controlls what is visual on the screen, the grid system and has the canvas. 

        :param width: The width of the window
        :param height: The height of the window
    """
    
    def __init__(self, width, height, mouse, keyboard, root):
        self.root = root
        self.keyboard = keyboard
        self.mouse = mouse

        self.width = width
        self.height = height
        self.offsetX = 0; self.realOffsetX = 0; self.bottomRightBorderX = 0
        self.offsetY = 0; self.realOffsetY = 0; self.bottomRightBorderY = 0
        self.totalZoom = 1
        self.gridSize = 25 # The value do not really matter for the reason that the user can zoom.'
        self.gridMode = True
        self.worldSize = 500

        self.setTitle()
        self.createCanvas()
        self.hoverBlock = self.canvas.create_rectangle(0, 0, self.gridSize, self.gridSize, fill="red")
        self.canvas.bind("<Configure>", self.updateScreenOnResize)
    
    def updateScreenOnResize(self, event):
        self.height = event.height
        self.width = event.width
        print(self.width)

    def createCanvas(self):
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(expand=1, side=LEFT, fill=BOTH)

    def setTitle(self):
        self.root.title("Game Of Life And DEATH!")

    def updateScreen(self):
        self.updateMouseGridPosition()
        self.updateCanvasOffset()

    def createCanvasGridLines(self):
        """
            Creates grid lines in the canvas. More easy to see the grid system the world is build upon
            :param worldSize: The size of the world.
        """
        worldSizeInPx = self.gridSize * self.worldSize
        self.vGrid = []
        for i in range(0, self.worldSize + 1):
            line = self.canvas.create_line(0, self.gridSize * i, worldSizeInPx, self.gridSize * i, fill="#333366")
            self.vGrid.append(line)

        self.hGrid = []
        for i in range(0, self.worldSize + 1):
            line = self.canvas.create_line(self.gridSize * i, 0, self.gridSize * i, worldSizeInPx, fill="#335566")
            self.hGrid.append(line)

        # for i in range(500):
        #     xPos = random.randint(0, 100) * self.gridSize
        #     yPos = random.randint(0, 100) * self.gridSize
        #     mycolor = '#%02x%02x%02x' % (50+ random.randint(0, 100), 200 + random.randint(0, 50), 200 + random.randint(0, 50)) 
        #     rect = self.canvas.create_rectangle(xPos, yPos, xPos + self.gridSize, yPos + self.gridSize, fill=mycolor, outline="")

    def updateCanvasOffset(self):
        """
            Updates the canvas offset. This handel the input from the user so that the user can move the canvas.
            :param worldSize: The size of the world.
        """
        # Offsert
        self.moveCanvasScreen(self.mouse.currentDragAmountX + self.mouse.totalDragAmountX, self.mouse.currentDragAmountY + self.mouse.totalDragAmountY)
    
        hoverX = self.mouse.xGridPos * self.gridSize * self.totalZoom + self.realOffsetX
        hoverY = self.mouse.yGridPos * self.gridSize * self.totalZoom + self.realOffsetY
        self.canvas.coords(self.hoverBlock, hoverX, hoverY, hoverX + self.gridSize * self.totalZoom, hoverY + self.gridSize * self.totalZoom)

        self.updateKeyboardInput()
        self.updateRealOffset()
        self.checkOffsetBorder()

    def updateMouseGridPosition(self):
        # Hover effect
        hoverX = (int((self.mouse.xPos - self.realOffsetX) / (self.gridSize * self.totalZoom))) 
        hoverY = (int((self.mouse.yPos - self.realOffsetY) / (self.gridSize * self.totalZoom)))
        self.mouse.updateGridPosition(hoverX, hoverY)

    def updateKeyboardInput(self):
        if(self.keyboard.addKey):
            self.zoomCanvasScreen(1.02)
        elif(self.keyboard.subtractKey):
            self.zoomCanvasScreen(0.98)

        if(self.keyboard.leftKey):
            self.offsetX -= self.width / 100
        if(self.keyboard.rightKey):
            self.offsetX += self.width / 100
        if(self.keyboard.upKey):
            self.offsetY -= self.width / 100
        if(self.keyboard.downKey):
            self.offsetY += self.width / 100

    def updateRealOffset(self):
        self.realOffsetX = self.canvas.coords(self.vGrid[0])[0]
        self.realOffsetY = self.canvas.coords(self.vGrid[0])[1]
        self.bottomRightBorderX = self.canvas.coords(self.vGrid[-1])[2]
        self.bottomRightBorderY = self.canvas.coords(self.vGrid[-1])[3]

    def checkOffsetBorder(self):
        checkPrecision = 100
        correctionSpeed = 0.20
        if(self.realOffsetX > 10/checkPrecision):
            self.offsetX += int(self.realOffsetX * correctionSpeed * checkPrecision) / checkPrecision
        if(self.realOffsetY > 10/checkPrecision):
            self.offsetY += int(self.realOffsetY * correctionSpeed * checkPrecision) / checkPrecision
        
        if(self.bottomRightBorderX - self.width < 10/checkPrecision):
            self.offsetX += int((self.bottomRightBorderX - self.width) * correctionSpeed * checkPrecision) / checkPrecision
        if(self.bottomRightBorderY - self.height < 10/checkPrecision):
            self.offsetY += int((self.bottomRightBorderY - self.height) * correctionSpeed * checkPrecision) / checkPrecision

    def moveCanvasScreen(self, xPos, yPos):
        moveX = xPos - self.offsetX
        moveY = yPos - self.offsetY
        if(abs(moveX) > 0 or abs(moveY) > 0):
            self.canvas.move(ALL, moveX, moveY)
            self.offsetX = xPos
            self.offsetY = yPos

    def changeGridStatus(self, mode):
        if(mode):
            state = "normal"
        else:
            state = "hidden"
        if(mode != self.gridMode):
            for vGrid in self.vGrid:
                self.canvas.itemconfig(vGrid, state=state)
            for hGrid in self.hGrid:
                self.canvas.itemconfig(hGrid, state=state)
        self.gridMode = mode

    def zoomCanvasScreen(self, amount):
        self.totalZoom *= amount
        if(self.totalZoom < 0.5):
            self.changeGridStatus(False)
        else:
            self.changeGridStatus(True)
        self.canvas.scale(ALL, int(self.width/2), int(self.height/2), amount, amount)
