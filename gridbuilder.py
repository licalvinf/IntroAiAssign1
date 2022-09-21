from tkinter import *
from random import sample, randint
from math import floor


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
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
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

        startx = randint(0, rowNumber-1)
        starty = randint(0, columnNumber-1)
        self.create_oval((startx * .5) * 50, (starty * 1.5) * 50, (startx * 1.5) * cellSize,
                         (starty * .5) * cellSize, fill="blue")

        print(startx)
        print(starty)

        goalx = randint(0, rowNumber-1)
        goaly = randint(0, columnNumber-1)
        self.create_oval((goalx * .9) * cellSize, (goaly * 1.1) * cellSize, (goalx * 1.1) * cellSize,
                         (goaly * .9) * cellSize, fill="red")

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        self.draw()

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


if __name__ == "__main__":
    app = Tk()
