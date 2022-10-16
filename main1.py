import graph
import display
import astar
import thetastar
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python main1.py graph_path")
    exit(1)
    
window = display.display(1600, 900)
g = graph.gridGraph(sys.argv[1])
window.update_graph(g)
window.run()
 
