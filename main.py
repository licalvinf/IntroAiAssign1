from random import randint
from tkinter import *
from tkinter import ttk
import gridbuilder





def astar(gridname, rows, cols, size):
    hvals = {}
    gvals = {}
    fvals = {}


root = Tk()
vrame = Frame(root, height=500, width=500)
cellsize = 10
numcols = 10
numrows = 10
# startcol = 2
# startrow = 3
grid = gridbuilder.CellGrid(root, numrows, numcols, cellsize)

# orad = .2
# oval = grid.create_oval((startcol*.9)*cellsize, (startrow*1.1)*cellsize, (startcol*1.1)*cellsize, (startrow*.9)*cellsize, fill="black")
grid.pack()

root.mainloop()


