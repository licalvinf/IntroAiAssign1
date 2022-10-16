from tkinter import *
from random import sample, randint
from math import floor
from heapq import heappop, heappush, heapify
import numpy
import random
import math

fringeDict = {}
closed = set()
startpoint = ()
endpoint = ()
grid = []


class Cell():
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size, blocked):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = blocked

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, file, *args, **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        if file is None:
            totalsize = rowNumber * columnNumber
            celllist = list(range(0, totalsize))
            filledcells = sample(celllist, floor(totalsize / 10))
            listiter = 0
            for row in range(rowNumber):

                line = []
                for column in range(columnNumber):
                    if listiter in filledcells:
                        line.append(Cell(self, column, row, cellSize, True))
                    else:
                        line.append(Cell(self, column, row, cellSize, False))
                    listiter += 1

                self.grid.append(line)

            # bind click action
            self.bind("<Button-1>", self.handleMouseClick)
            self.draw()

            startendpts = self.pointmaker(rowNumber, columnNumber, 10)
            startpt = (startendpts[0], startendpts[1])
            endpt = (startendpts[2], startendpts[3])
            self.a_Star(startpt, endpt, cellSize)
        else:
            griddata = open(file)
            start = griddata.readline()
            goal = griddata.readline()

            sizedata = griddata.readline()
            columnNumber = int(sizedata[0])
            rowNumber = int(sizedata[2])
            tiledata = griddata.readline()

            for row in range(rowNumber):
                line = []
                for column in range(columnNumber):
                    line.append(Cell(self, column, row, cellSize, False))
                self.grid.append(line)
            while tiledata:
                if int(tiledata[4]) == 1:
                    self.grid[int(tiledata[2]) - 1][int(tiledata[0]) - 1].fill = True
                tiledata = griddata.readline()

            self.bind("<Button-1>", self.handleMouseClick)
            self.draw()

            self.create_oval((int(start[0]) - 1) * cellSize - 5, (int(start[2]) - 1) * cellSize + 5,
                             (int(start[0]) - 1) * cellSize + 5,
                             (int(start[2]) - 1) * cellSize - 5, fill="blue")

            self.create_oval((int(goal[0]) - 1) * cellSize - 5, (int(goal[2]) - 1) * cellSize + 5,
                             (int(goal[0]) - 1) * cellSize + 5,
                             (int(goal[2]) - 1) * cellSize - 5, fill="red")

            startpt = ((int(start[2]) - 1), (int(start[0]) - 1))
            endpt = ((int(goal[2]) - 1), (int(goal[0]) - 1))

            print("Start: ")
            print(startpt)
            print("End: ")
            print(endpt)
            self.a_Star(startpt, endpt, cellSize)

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        print('vertex: (' + str(cell.abs) + ", " + str(cell.ord) + ")")
        print('vertex: (' + str(cell.abs + 1) + ", " + str(cell.ord) + ")")
        print('vertex: (' + str(cell.abs) + ", " + str(cell.ord + 1) + ")")
        print('vertex: (' + str(cell.abs + 1) + ", " + str(cell.ord + 1) + ")")

    def pointmaker(self, rows, cols, size):
        rowNumber = rows
        columnNumber = cols
        cellSize = size
        pathblocked = True
        while pathblocked is True:
            startrow = randint(0, rowNumber - 1)
            startcol = randint(0, columnNumber - 1)
            goalrow = randint(0, rowNumber - 1)
            goalcol = randint(0, columnNumber - 1)

            startcol = 25
            startrow = 25
            goalcol = 75
            goalrow = 25

            for col in range(startcol, goalcol):
                pathblocked = True
                for row in range(rows):
                    if self.grid[row][col].fill is not True:
                        pathblocked = False
                        break
            if pathblocked is True:
                continue
            for row in range(startrow, goalrow):
                pathblocked = True
                for col in range(cols):
                    if self.grid[row][col].fill is not True:
                        pathblocked = False
                        break

        self.create_oval(startcol * cellSize - 5, startrow * cellSize + 5, startcol * cellSize + 5,
                         startrow * cellSize - 5, fill="blue")

        self.create_oval(goalcol * cellSize - 5, goalrow * cellSize + 5, goalcol * cellSize + 5,
                         goalrow * cellSize - 5, fill="red")
        return startrow, startcol, goalrow, goalcol

    # Computes heuristic for A*
    def a_Star_Heuristic(self, currentPoint, endPoint):
        diagonal = math.sqrt(2) * min(abs(currentPoint[0] - endPoint[0]), abs(currentPoint[1] - endPoint[1]))
        cardinal = max(abs(currentPoint[0] - endPoint[0]), abs(currentPoint[1] - endPoint[1])) - min(
            abs(currentPoint[0] - endPoint[0]), abs(currentPoint[1] - endPoint[1]))
        h = diagonal + cardinal
        return h

    def a_Star(self, startpoint, endpoint, size):
        global fringe
        global closed
        # Sets up the heuristic for all points
        heuristic = {}

        # Sets up array of tuples to track parents
        parent = {}

        # g is used to notate the distance from start to point
        g = {}

        # fringe holds the next node to visit based off of f
        # f is g + heuristic
        f = {}

        fringe = []
        heapify(fringe)

        g.update({startpoint: 0})
        parent.update({startpoint: startpoint})
        h = self.a_Star_Heuristic(startpoint, endpoint)
        heuristic.update({startpoint: h})
        fringeDict.update({startpoint: g.get(startpoint) + heuristic.get(startpoint)})
        heappush(fringe, (fringeDict.get(startpoint), startpoint[0], startpoint[1]))
        print(len(self.grid))
        print(len(self.grid[0]))
        fringeDict.update({startpoint: g.get(startpoint) + heuristic.get(startpoint)})
        while (len(fringe) is not 0):
            currentpoint = heappop(fringe)
            currentpoint = (currentpoint[1], currentpoint[2])
            print("Current point:")
            print(currentpoint)
            if (currentpoint == endpoint):
                point = endpoint
                lst = [endpoint]
                print("Path is:")
                while (parent.get(point) is not startpoint):
                    lst.insert(0, parent.get(point))
                    point = parent.get(point)
                self.create_line(10, 40, 20, 50)
                for i in range(len(lst) - 1):
                    self.create_line(lst[i][1] * size, lst[i][0] * size, lst[i + 1][1] * size, lst[i + 1][0] * size,
                                     width=3, fill='blue')
                for x in lst:
                    print(x)
                for key, value in fringeDict.items():
                    print(key, value)
                print("heuristic")
                for key1, value1 in heuristic.items():
                    print(key1, value1)
                return "Path found"
            else:
                closed.add(currentpoint)
                if (currentpoint[1] - 1 >= 0):  # Check the points to the left of the current point
                    if (currentpoint[0] - 1 >= 0):  # Check point diagonally up left
                        checkpoint = (currentpoint[0] - 1, currentpoint[1] - 1)
                        print("Up Left:{}".format(checkpoint))
                        if (self.grid[currentpoint[0] - 1][
                            currentpoint[1] - 1].fill is False):  # Check if path is clear
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    if (currentpoint[0] + 1) <= len(self.grid):  # Check the point diagonally down left
                        checkpoint = (currentpoint[0] + 1, currentpoint[1] - 1)
                        print("Down Left:{}".format(checkpoint))
                        if (self.grid[currentpoint[0]][currentpoint[1] - 1].fill is False):  # Check if path is clear
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    checkpoint = (currentpoint[0], currentpoint[1] - 1)  # Check the point to the left
                    print("Left:{}".format(checkpoint))
                    if ((currentpoint[0] is 0 and self.grid[currentpoint[0]][currentpoint[1] - 1].fill is False) or (
                            currentpoint[0] is len(self.grid) and self.grid[currentpoint[0] - 1][
                        currentpoint[1] - 1].fill is False) or (
                            currentpoint[0] is not 0 and currentpoint[0] is not len(self.grid) and
                            self.grid[currentpoint[0] - 1][currentpoint[1] - 1] is False and self.grid[currentpoint[0]][
                                currentpoint[1] - 1] is False)):  # Check if path is clear
                        if checkpoint not in closed:  # Check if it is closed
                            if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                parent.update({checkpoint: None})
                            if g.get(currentpoint) + 1 < g.get(checkpoint):
                                g.update({checkpoint: g.get(currentpoint) + 1})
                                parent.update({checkpoint: currentpoint})
                                if fringeDict.get(checkpoint) is not None:
                                    fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                    heapify(fringe)
                                heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                heappush(fringe, checkpoint)

                if (currentpoint[1] + 1 <= len(self.grid[0])):  # Check the points to the right of the current point
                    if (currentpoint[0] - 1 >= 0):  # Check point diagonally up right
                        checkpoint = (currentpoint[0] - 1, currentpoint[1] + 1)
                        print("Up Right:{}".format(checkpoint))
                        if (self.grid[currentpoint[0] - 1][currentpoint[1]].fill is False):  # Check if path is clear
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    if (currentpoint[0] + 1 <= len(self.grid)):  # Check point diagonally down right
                        checkpoint = (currentpoint[0] + 1, currentpoint[1] + 1)
                        print("Down Right:{}".format(checkpoint))
                        if (self.grid[currentpoint[0]][currentpoint[1]].fill is False):  # Check if path is clear
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + math.sqrt(2) < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + math.sqrt(2)})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    checkpoint = (currentpoint[0], currentpoint[1] + 1)  # Check the point to the right
                    print("Right:{}".format(checkpoint))
                    if ((currentpoint[0] is 0 and self.grid[currentpoint[0]][currentpoint[1]].fill is False) or (
                            currentpoint[0] is len(self.grid) and self.grid[currentpoint[0] - 1][
                        currentpoint[1]] is False) or (
                            currentpoint[0] is not 0 and currentpoint[0] is not len(self.grid) and
                            self.grid[currentpoint[0] - 1][currentpoint[1]].fill is False and
                            self.grid[currentpoint[0]][
                                currentpoint[1]].fill is False)):  # Check if path is clear
                        if checkpoint not in closed:  # Check if it is closed
                            if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                parent.update({checkpoint: None})
                            if g.get(currentpoint) + 1 < g.get(checkpoint):
                                g.update({checkpoint: g.get(currentpoint) + 1})
                                parent.update({checkpoint: currentpoint})
                                if fringeDict.get(checkpoint) is not None:
                                    fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                    heapify(fringe)
                                heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                heappush(fringe, checkpoint)

                    checkpoint = (currentpoint[0] - 1, currentpoint[1])  # Check the point above
                    print("Up:{}".format(checkpoint))
                    if currentpoint[0] - 1 >= 0:
                        if ((currentpoint[1] is 0 and self.grid[currentpoint[0] - 1][
                            currentpoint[1]].fill is False) or (
                                currentpoint[1] is len(self.grid[0]) and self.grid[currentpoint[0] - 1][
                            currentpoint[1] - 1].fill is False) or (
                                currentpoint[1] is not 0 and currentpoint[1] is not len(self.grid[0]) and
                                self.grid[currentpoint[0] - 1][currentpoint[1]].fill is False and
                                self.grid[currentpoint[0] - 1][currentpoint[1]].fill is False)):
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + 1 < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + 1})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)

                    checkpoint = (currentpoint[0], currentpoint[1] + 1)  # Check the point to the bottom
                    print("Right:{}".format(checkpoint))
                    if currentpoint[0] + 1 <= len(self.grid):
                        if ((currentpoint[1] is 0 and self.grid[currentpoint[0]][currentpoint[1]] is False) or (currentpoint[1] is len(self.grid[0]) and self.grid[currentpoint[0]][currentpoint[1]-1] is False) or (currentpoint[1] is not 0 and currentpoint[1] is not len(self.grid[0]) and (self.grid[currentpoint[0]][currentpoint[1]] is False or self.grid[currentpoint[0]][currentpoint[1]-1] is False))):
                            if checkpoint not in closed:  # Check if it is closed
                                if fringeDict.get(checkpoint) is None:  # Check if the point is in fringe already
                                    g.update({checkpoint: numpy.inf})  # If not in fringe, add it to the fringe
                                    parent.update({checkpoint: None})
                                if g.get(currentpoint) + 1 < g.get(checkpoint):
                                    g.update({checkpoint: g.get(currentpoint) + 1})
                                    parent.update({checkpoint: currentpoint})
                                    if fringeDict.get(checkpoint) is not None:
                                        fringe.remove((fringeDict.get(checkpoint), checkpoint[0], checkpoint[1]))
                                        heapify(fringe)
                                    heuristic.update({checkpoint: self.a_Star_Heuristic(checkpoint, endpoint)})
                                    fringeDict.update({checkpoint: g.get(checkpoint) + heuristic.get(checkpoint)})
                                    checkpoint = (fringeDict.get(checkpoint), checkpoint[0], checkpoint[1])
                                    heappush(fringe, checkpoint)


if __name__ == "__main__":
    app = Tk()
