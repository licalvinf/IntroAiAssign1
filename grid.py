from itertools import product
from random import sample
from heapq import heappop, heappush, heapify
import numpy
import random
import math

#Create global variables
fringeDict = {}
closed = set()
startpoint = ()
endpoint = ()
obstacles = []

class Grid:
    def __init__ (self, rows, cols): 
        global startpoint
        global endpoint
        global obstacles
        #Uses user input to create a grid of any size
        rowRange = range(0,rows-1)
        colRange = range(0,cols-1)
        
        #Randomly generates coordinates to block off on the grid
        #10% of total grid is blocked off
        blockLocation = random.sample(list(product(rowRange,colRange)),int(rows * cols * .1))
        
        #Sets up a 2D array to refer to locations of walls
        #0 is free, 1 is blocked
        obstacles= [[0 for x in range(rows)] for y in range(cols)]
        for wall in blockLocation:
            obstacles[wall[0]][wall[1]] = 1
            
        #Chooses random placements for start and end, 0 to 150 inclusive
        startpoint = (random.randint(0,rows), random.randint(0,cols))
        endpoint = (random.randint(0,rows), random.randint(0,cols))
        
    #Computes heuristic for A*
    def a_Star_Heuristic(self, currentPoint, endPoint):
        diagonal = math.sqrt(2) * min(abs(currentPoint[0]-endPoint[0]), abs(currentPoint[1] - endPoint[1]))
        cardinal = max(abs(currentPoint[0]-endPoint[0]), abs(currentPoint[1] - endPoint[1])) - min(abs(currentPoint[0]-endPoint[0]), abs(currentPoint[1] - endPoint[1]))
        h = diagonal + cardinal
        return h

    def a_Star(self):
        global fringe
        global closed
        #Sets up the heuristic for all points
        heuristic = {}
        
        #Sets up array of tuples to track parents
        parent = {}
        
        #g is used to notate the distance from start to point
        g = {}

        fringe = []
        heapify(fringe)

        g.update({startpoint:0})
        parent.update({startpoint:startpoint})
        h = self.a_Star_Heuristic(startpoint, endpoint)
        heuristic.update({startpoint:h})
        fringeDict.update({startpoint: g.get(startpoint) + heuristic.get(startpoint)})
        heappush(fringe,(fringeDict.get(startpoint),startpoint[0],startpoint[1]))
        print(startpoint)
        print(endpoint)
        for row in obstacles:
          print(row)
        fringeDict.update({startpoint: g.get(startpoint) + heuristic.get(startpoint)})
        while(len(fringe) is not 0):
            currentpoint = heappop(fringe)
            currentpoint = (currentpoint[1],currentpoint[2])
            print(currentpoint)
            if (currentpoint == endpoint):
                point = endpoint
                lst = [endpoint]
                print("Path is:")
                while (parent.get(point) is not startpoint):
                    lst.insert(0,parent.get(point))
                    point = parent.get(point)
                for x in lst:
                    print(x)
                return "Path found"
            else:
                closed.add(currentpoint)
                if (currentpoint[1] - 1 >= 0): #Check the points to the left of the current point
                    if (currentpoint[0] - 1 >= 0): #Check point diagonally up left
                        checkpoint = (currentpoint[0]-1, currentpoint[1]-1)
                        if (obstacles[currentpoint[0]-1][currentpoint[1]-1] == 0): #Check if path is clear
                            if checkpoint not in closed: #Check if it is closed
                                if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint)+math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)
                                    

                    if (currentpoint[0] + 1) <= len(obstacles): #Check the point diagonally down left
                      checkpoint = (currentpoint[0]+1, currentpoint[1]-1)
                      if (obstacles[currentpoint[0]][currentpoint[1]-1] == 0): #Check if path is clear
                            if checkpoint not in closed: #Check if it is closed
                                if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint)+math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)
    
                    checkpoint = (currentpoint[0], currentpoint[1]-1) #Check the point to the left
                    if ((currentpoint[0] is 0 and obstacles[currentpoint[0]][currentpoint[1] - 1] is 0) or (currentpoint[0] is len(obstacles) and obstacles[currentpoint[0]-1][currentpoint[1]-1] is 0) or (currentpoint[0] is not 0 and currentpoint[0] is not len(obstacles) and (obstacles[currentpoint[0]-1][currentpoint[1]-1] is 0 or obstacles[currentpoint[0]][currentpoint[1] - 1] is 0))): #Check if path is clear
                          if checkpoint not in closed: #Check if it is closed
                                if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                   g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                   parent.update({checkpoint: None})
                                if g.get(currentpoint) + 1 < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint)+ 1})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                if (currentpoint[1] + 1 <= len(obstacles)): #Check the points to the right of the current point
                    if (currentpoint[0] - 1 >= 0): #Check point diagonally up right
                        checkpoint = (currentpoint[0]-1, currentpoint[1]+1)
                        if (obstacles[currentpoint[0]-1][currentpoint[1]] == 0): #Check if path is clear
                            if checkpoint not in closed: #Check if it is closed
                                if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint)+math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    if (currentpoint[0] + 1 <= len(obstacles)): #Check point diagonally down right
                        checkpoint = (currentpoint[0]+1, currentpoint[1]+1)
                        if (obstacles[currentpoint[0]][currentpoint[1]] == 0): #Check if path is clear
                            if checkpoint not in closed: #Check if it is closed
                                if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint)+math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)
                    
                    checkpoint = (currentpoint[0], currentpoint[1]+1) #Check the point to the right
                    if ((currentpoint[0] is 0 and obstacles[currentpoint[0]][currentpoint[1]] is 0) or (currentpoint[0] is len(obstacles[0]) and obstacles[currentpoint[0]-1][currentpoint[1]] is 0) or (currentpoint[0] is not 0 and currentpoint[0] is not len(obstacles[0]) and (obstacles[currentpoint[0]-1][currentpoint[1]] is 0 or obstacles[currentpoint[0]][currentpoint[1]] is 0))): #Check if path is clear
                        if checkpoint not in closed: #Check if it is closed
                            if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                parent.update({checkpoint: None})
                            if g.get(currentpoint) + 1 < g.get(checkpoint):
                                g.update({checkpoint: g.get(currentpoint) + 1})
                                parent.update({checkpoint: currentpoint})
                                if fringeDict.get(checkpoint) is not None:
                                    fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                    heapify(fringe)
                                heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                heappush(fringe, checkpoint)

                    checkpoint = (currentpoint[0]-1, currentpoint[1]) #Check the point above
                    if currentpoint[0] - 1 >= 0:
                        if ((currentpoint[1] is 0 and obstacles[currentpoint[0]-1][currentpoint[1]] is 0) or (currentpoint[1] is len(obstacles[0]) and obstacles[currentpoint[0]-1][currentpoint[1]-1] is 0) or (currentpoint[1] is not 0 and currentpoint[1] is not len(obstacles) and (obstacles[currentpoint[0]-1][currentpoint[1]] is 0 or obstacles[currentpoint[0]-1][currentpoint[1]] is 0))):
                          if checkpoint not in closed: #Check if it is closed
                            if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                parent.update({checkpoint: None})
                            if g.get(currentpoint) + 1 < g.get(checkpoint):
                                g.update({checkpoint: g.get(currentpoint) + 1})
                                parent.update({checkpoint: currentpoint})
                                if fringeDict.get(checkpoint) is not None:
                                    fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                    heapify(fringe)
                                heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                heappush(fringe, checkpoint)
                    
                    checkpoint = (currentpoint[0] + 1, currentpoint[1]) #Check the point to the bottom
                    if currentpoint[0] + 1 <= len(obstacles):
                        if ((currentpoint[1] is 0 and obstacles[currentpoint[0]][currentpoint[1]] is 0) or (currentpoint[1] is len(obstacles[0]) and obstacles[currentpoint[0]][currentpoint[1]-1] is 0) or (currentpoint[1] is not 0 and currentpoint[1] is not len(obstacles) and (obstacles[currentpoint[0]][currentpoint[1]] is 0 or obstacles[currentpoint[0]][currentpoint[1]-1] is 0))):
                          if checkpoint not in closed: #Check if it is closed
                            if fringeDict.get(checkpoint) is None: # Check if the point is in fringe already
                                g.update({checkpoint: numpy.inf}) # If not in fringe, add it to the fringe
                                parent.update({checkpoint: None})
                            if g.get(currentpoint) + 1 < g.get(checkpoint):
                                g.update({checkpoint: g.get(currentpoint) + 1})
                                parent.update({checkpoint: currentpoint})
                                if fringeDict.get(checkpoint) is not None:
                                    fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                    heapify(fringe)
                                heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint,endpoint)})
                                fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                heappush(fringe, checkpoint)

def main():
    grid = Grid(5,10)
    grid.a_Star()

if __name__ == "__main__":
    main()
