from random import randint
from tkinter import *
from tkinter import ttk
import gridbuilder


def pointmaker(gridname, rows, cols, size):
    rowNumber = rows
    columnNumber = cols
    cellSize = size
    cellgrid = gridname
    pathblocked = True
    while pathblocked is True:
        startrow = randint(0, rowNumber - 1)
        startcol = randint(0, columnNumber - 1)
        goalrow = randint(0, rowNumber - 1)
        goalcol = randint(0, columnNumber - 1)

        for col in range(startcol, goalcol):
            pathblocked = True
            for row in range(rows):
                if cellgrid.grid[row][col].fill is not True:
                    pathblocked = False
                    break
        if pathblocked is True:
            continue
        for row in range(startrow, goalrow):
            pathblocked = True
            for col in range(cols):
                if cellgrid.grid[row][col].fill is not True:
                    pathblocked = False
                    break

    cellgrid.create_oval(startcol * cellSize-5, startrow * cellSize+5, startcol * cellSize+5,
                     startrow * cellSize-5, fill="blue")

    cellgrid.create_oval(goalcol * cellSize-5, goalrow * cellSize+5, goalcol * cellSize+5,
                     goalrow * cellSize-5, fill="red")



root = Tk()
vrame = Frame(root, height=500, width=500)
cellsize = 10
numrows = 50
numcols = 100
# startcol = 2
# startrow = 3
grid = gridbuilder.CellGrid(root, numrows, numcols, cellsize)
pointmaker(grid, numrows, numcols, cellsize)
# orad = .2
# oval = grid.create_oval((startcol*.9)*cellsize, (startrow*1.1)*cellsize, (startcol*1.1)*cellsize, (startrow*.9)*cellsize, fill="black")
grid.pack()

root.mainloop()

