from manim import *
from manim import config
import random
import time

#cell x starts from 1 (0 is boundry) and grows to the right
#cell y starts from 1 (0 is boundry) and grows upwards
#calculate edge from cell indices:
#left: cell.x, down: cell.y, right: cell.x+1, up: cell.y+1
displayWidth = 1920
displayHeight = 1080

class DFSLabirynth():
  def __init__(self):
    self.stack = []  #from numOfCellsInRow increase to the right and then every row up is + (row+2) count
    self.visited = []
    #animation trace variables: (all accessess in labirynth and listFree methods)
    self.verticesOrdered = []  #tuples
    self.freeNeighborsOrdered = [] #lists
    self.edgeRemovalsOrdered = [] #numbers
    self.goingBack = []  #tuples
    #everything underneath is setting boudries to True and center to False
    self.visited.append((numOfCellsInColumn+2)*[True])  #if vertex visited
    for column in range(1, numOfCellsInRow+1):
      self.visited.append([True])
      for row in range(1, numOfCellsInColumn+1):
        self.visited[column].append(False)
      self.visited[column].append(True)
    self.visited.append((numOfCellsInColumn+2)*[True])
  # def stackIndex(self, x, y):
  #   return y*(numOfCellsInRow+2)+x+1
  # def coordsFromStackIndex(self, n):
  #   return [int(n/(numOfCellsInRow+2)), (n%(numOfCellsInColumn+2))-1]
  def startingPoint(self):
    if(numOfCellsInRow > 1):
      x = random.randrange(1, numOfCellsInRow)
    else:
      x = 1
    if(numOfCellsInColumn > 1):
      y = random.randrange(1, numOfCellsInColumn)
    else:
      y = 1
    # print(x, y)
    # print(self.visited)
    self.visited[x][y] = True
    self.stack.append((x, y))
    return [x, y]
  def listFree(self, x, y):
    # print("list free:" + str(x) + " " + str(y) + " " + str(self.visited[x-1][y]) + " " + str(self.visited[x][y-1]) + " " + str(self.visited[x][y+1]) + " " + str(self.visited[x][y+1]) + " ")
    freeNeighbors = []
    coords = [] #for animation purposes only
    if(not self.visited[x-1][y]):
      freeNeighbors.append(0)
      coords.append((x-1, y))
    if(not self.visited[x][y-1]):
      freeNeighbors.append(1)
      coords.append((x, y-1))
    if(not self.visited[x+1][y]):
      freeNeighbors.append(2)
      coords.append((x+1, y))
    if(not self.visited[x][y+1]):
      freeNeighbors.append(3)
      coords.append((x, y+1))
    self.freeNeighborsOrdered.append(coords)
    return freeNeighbors
  def direction(self, direct, x, y):  # 0 is left, 1 is down, 2 is right, 3 is up
    if(direct == 0):
      return [x-1, y]
    if(direct == 1):
      return [x, y-1]
    if(direct == 2):
      return [x+1, y]
    return [x, y+1]
  def labirynth(self, startingPoint):
    # print(self.stack)
    [x, y] = startingPoint
    self.verticesOrdered.append((x, y))
    while(True):
      # print("ff: " + str(x) + " " + str(y))
      neighbors = self.listFree(x, y)
      if(neighbors):
        choosen = random.choice(neighbors)
        self.edgeRemovalsOrdered.append(choosen)
        [x, y] = self.direction(choosen, x, y)
        self.verticesOrdered.append((x, y))
        self.stack.append((x, y))
        self.visited[x][y] = True
      else: #no neighbors
        if(self.stack):
          # print("stack size: " + str(len(self.stack)))
          # print(self.stack)
          (x, y) = self.stack.pop()
          self.goingBack.append((x, y))
          # print("pop " + str(x) + " " + str(y))
        else:
          break
    return [x, y]
  def giveAlgorithmTrace(self):
    return (self.verticesOrdered, self.freeNeighborsOrdered,
            self.edgeRemovalsOrdered, self.goingBack)

class MathGrid:
  def __init__(self, numOfCellsInRow, numOfCellsInColumn, cellSize):
    self.numOfCellsInRow = numOfCellsInRow
    self.numOfCellsInColumn = numOfCellsInColumn
    self.cellSize = cellSize
  #calculations coordinate system: [..., ...] -> [-1, 1]
  def genBaseGrid(self):
    #1.index is x, 2. is y, 3rd is beginning(2 points) and end(2 points) of line
    vlines = [] #vertical; [[[]]] actually
    hlines = [] #horizontal; [[[]]] actually
    tvrow = [] #temp v row; [[]] actually
    throw = [] #temp h row; [[]] actually
    for row in range(numOfCellsInColumn):
      tvrow.clear()
      throw.clear()
      for column in range(numOfCellsInRow):
        tvrow.append([
          -displayWidth/2 + column * cellSize,
          -displayHeight/2 + row * cellSize,
          -displayWidth/2 + column * cellSize,
          -displayHeight/2 + (row+1) * cellSize,
        ])
        throw.append([
          -displayWidth/2 + column * cellSize,
          -displayHeight/2 + row * cellSize,
          -displayWidth/2 + (column+1) * cellSize,
          -displayHeight/2 + row * cellSize,
        ])
      vlines.append(tvrow.copy())
      hlines.append(throw.copy())
    return [vlines, hlines]
  
# ========== MANIM PART UNDERNEATH ==========
# animating coordinate system: width: [-1, 1] -> [-7, 7]
# height: [-1, 1] -> [-3.9, 3.9]
# quality must be one of ['fourk_quality', 'production_quality',
# 'high_quality', 'medium_quality', 'low_quality', 'example_quality']
# config.quality = "medium_quality"
config.quality = "high_quality"

class AnimatedAlgorithm(Scene):
  def dontOverrideManimInit(self, numOfCellsInRow, numOfCellsInColumn, cellSize, RTM):
    self.numOfCellsInRow = numOfCellsInRow
    self.numOfCellsInColumn = numOfCellsInColumn
    self.cellSize = cellSize
    self.RTM = RTM
    self.xScale = 7/(displayWidth/2)
    self.yScale = 3.9/(displayHeight/2)
    self.vlines = [] #vertical; [[[]]] actually
    self.hlines = [] #horizontal; [[[]]] actually
    self.vlo = []   #vertival line objects; [[]] actually
    self.hlo = []   #horizontal line objects; [[]] actually
    #algorithm trace variables:
    self.verticesOrdered = []  #tuples
    self.freeNeighborsOrdered = [] #lists
    self.edgeRemovalsOrdered = [] #numbers
    self.goingBack = []  #tuples
    #outer vertical (& horizontal) line object
    self.ovlo = Line([(-displayWidth/2+numOfCellsInRow*cellSize)*self.xScale,
                (-displayHeight/2)*self.yScale, 0],
                [(-displayWidth/2+numOfCellsInRow*cellSize)*self.xScale,
                (-displayHeight/2+numOfCellsInColumn*cellSize)*self.yScale, 0])
    self.ohlo = Line([(-displayWidth/2+numOfCellsInRow*cellSize)*self.xScale,
                (-displayHeight/2+numOfCellsInColumn*cellSize)*self.yScale, 0],
                [(-displayWidth/2)*self.xScale,
                (-displayHeight/2+numOfCellsInColumn*cellSize)*self.yScale, 0])
  def createLineObjects(self):
    tvrow = [[]] #temp v row
    for row in self.vlines:
      tvrow.clear()
      for column in row:
        tvrow.append(Line([column[0]*self.xScale, column[1]*self.yScale, 0],
                          [column[2]*self.xScale, column[3]*self.yScale, 0]))
      self.vlo.append(tvrow.copy())
    throw = [[]] #temp h row
    for row in self.hlines:
      throw.clear()
      for column in row:
        throw.append(Line([column[0]*self.xScale, column[1]*self.yScale, 0],
                          [column[2]*self.xScale, column[3]*self.yScale, 0]))
      self.hlo.append(throw.copy())
  def xAlgoScale(self, x):
    return -7 + x*cellSize*self.xScale-cellSize*self.xScale/2
  def yAlgoScale(self, y):
    return -3.9 + y*cellSize*self.yScale-cellSize*self.yScale/2
  def updateCellColor(self, x, y):
    return Rectangle(
      width=cellSize*self.xScale-0.04, height=cellSize*self.yScale-0.04,
      ).move_to(Point([self.xAlgoScale(x), self.yAlgoScale(y), 0])
      ).set_stroke(width=0)
  def construct(self):
    self.play(Create(self.ovlo), run_time = self.RTM)
    self.play(Create(self.ohlo), run_time = self.RTM)
    fadeInGrid = []
    for row in range(self.numOfCellsInColumn):
      for column in range(self.numOfCellsInRow):
        fadeInGrid.append(FadeIn(self.vlo[row][column]))
        fadeInGrid.append(FadeIn(self.hlo[row][column]))
    self.play(*fadeInGrid, run_time=0.5, rate_func=linear)
    wiggleGrid = [Wiggle(self.ovlo), Wiggle(self.ohlo)]
    for row in range(self.numOfCellsInColumn):
      for column in range(self.numOfCellsInRow):
        wiggleGrid.append(Wiggle(self.vlo[row][column]))
        wiggleGrid.append(Wiggle(self.hlo[row][column]))
    self.play(*wiggleGrid, run_time = 2, rate_func=rate_functions.double_smooth)
    #here starts with input from algorithm
    # start/end - red, new cell - green,
    # potential neighbor - yellow, go back - blue
    self.verticesOrdered.reverse()
    self.freeNeighborsOrdered.reverse()
    self.edgeRemovalsOrdered.reverse()
    self.goingBack.reverse()
    numOfCells = self.numOfCellsInColumn*self.numOfCellsInRow
    x, y = self.verticesOrdered.pop()
    self.play(self.updateCellColor(x, y).animate.set_fill(RED, opacity=1))
    numOfCells -= 1
    groupAnimations = []
    saveToHide = []
    while(numOfCells):
      neigbors = self.freeNeighborsOrdered.pop()
      groupAnimations.clear()
      saveToHide.clear()
      if(neigbors):
        for neigbor in neigbors:
          x, y = neigbor
          showAndHide = self.updateCellColor(x, y)
          saveToHide.append(showAndHide)
          groupAnimations.append(showAndHide.animate.set_fill(YELLOW, opacity=0.7))
        self.play(*groupAnimations, run_time = self.RTM*0.25)
        groupAnimations.clear()
        for toHide in saveToHide:
          groupAnimations.append(FadeOut(toHide))
        self.play(*groupAnimations, run_time = self.RTM*0.25)
        x, y = self.verticesOrdered.pop()
        numOfCells-=1
        groupAnimations.clear()
        match(self.edgeRemovalsOrdered.pop()):
          case 0:
            groupAnimations.append(FadeOut(self.vlo[y-1][x]))
          case 1:
            groupAnimations.append(FadeOut(self.hlo[y][x-1]))
          case 2:
            groupAnimations.append(FadeOut(self.vlo[y-1][x-1]))
          case 3:
            groupAnimations.append(FadeOut(self.hlo[y-1][x-1]))
        showAndHide = self.updateCellColor(x, y)
        groupAnimations.append(showAndHide.animate.set_fill(GREEN, opacity=1))
        self.play(*groupAnimations, run_time = self.RTM)
        self.play(FadeOut(showAndHide), run_time = self.RTM*0.25)
      else:
        x, y = self.goingBack.pop()
        showAndHide = self.updateCellColor(x, y)
        self.play(showAndHide.animate.set_fill(BLUE, opacity=1), run_time = self.RTM*0.25)
        self.play(FadeOut(showAndHide), run_time = self.RTM*0.25)
    self.wait(3)

# ========== MAIN MANAGEMENT SPACE ==========

if __name__ == '__main__':
  numOfCellsInRow = int(input("Enter number of cells in a row: "))
  numOfCellsInColumn = int(input("Enter number of cells in a column: "))
  cellSize = min(displayHeight/numOfCellsInColumn, displayWidth/numOfCellsInRow)
  RTM = float(input("Enter animation speed (e.g. 1): "))  # run_time multiplier
  start = time.time()
  animation = AnimatedAlgorithm()
  animation.dontOverrideManimInit(numOfCellsInRow, numOfCellsInColumn, cellSize, RTM)
  [animation.vlines, animation.hlines] = MathGrid(numOfCellsInRow, numOfCellsInColumn, cellSize).genBaseGrid()
  animation.createLineObjects()
  algoStart = time.time()
  algorithm = DFSLabirynth()
  algorithm.labirynth(algorithm.startingPoint())
  passArgsStart = time.time()
  (animation.verticesOrdered,
   animation.freeNeighborsOrdered,
   animation.edgeRemovalsOrdered,
   animation.goingBack) = algorithm.giveAlgorithmTrace()
  animationStart = time.time()
  animation.render(preview=True)
  animationEnd = time.time()
  print("Video quality: " + config.quality)
  print("How long did it take in seconds:")
  print("Animation grid preparation: " + str(round(algoStart-start, 3)))
  print("Purely logical part of algorithm generation: " + str(round(passArgsStart-algoStart, 2)))
  print("Passing animation data from algorithm: " + str(round(animationStart-passArgsStart, 2)))
  print("Animation rendering: " + str(round(animationEnd-animationStart, 2)))
  print("Whole process from start to end: " + str(round(animationEnd-start, 2)))
