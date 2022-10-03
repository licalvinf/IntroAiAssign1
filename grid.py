from itertools import product
from random import sample
import numpy
import math

class Grid:
    def __init__ (self, rows, cols): 
        #Uses user input to create a grid of any size
        rowRange = range(0,rows-1)
        colRange = range(0,cols-1)
        
        #Randomly generates coordinates to block off on the grid
        #10% of total grid is blocked off
        blockLocation = random.sample(list(itertools.product(rowRange,colRange)),int(rows * cols * .1))
        
        #Sets up a 2D array to refer to locations of walls
        #0 is free, 1 is blocked
        self.obstacles= [[0 for x in range(rows-1)] for y in range(cols-1)]
        for wall in blockLocation:
            obstacles[wall[0]][wall[1]] = 1
            
        #Chooses random placements for start and end
        startpoint = (random.randint(0,150), random.randint(0,150))
        endpoint = (random.randint(0,150), random.randint(0,150))
        
        
def a_Star:
    #Sets up the heuristic for all points - initially set to inf
        self.heuristic = [[numpy.inf for x in range(rows)] for y in range(cols)]
        
        #Sets up array of tuples to track parents
        self.parents = [[(numpy.inf, numpy.inf) for x in range(rows)] for y in range(cols)]
        
        #g is used to notate the distance from start to point
        self.g =  [[numpy.inf for x in range(rows)] for y in range(cols)]
        
        
 
#Comparitive method to use in binary heap
#Allows tuples to be placed in the heap and compared by their 
def __lt__(self, other):
    return self.intAttribute < other.intAttribute
