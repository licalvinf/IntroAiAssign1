import math

class Edge():
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

class Node():
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.blocked = blocked
        self.closed = False

class gridGraph():
        def __init__(self,f):
            self.nodes = []
            self.vis_edges = None
            self.width = 10
            self.height = 10
            self.edges = dict()
            self.src = None
            self.dst = None
            self.read_graph(f)
           

        def read_graph(self,fi):
            with open(fi, 'r') as f:
                line = f.readline().strip().split()
                self.src = (int(line[0]) - 1, int(line[1]) - 1)
                line = f.readline().strip().split()
                self.dst = (int(line[0]) - 1, int(line[1]) - 1)
                line = f.readline().strip().split()
                self.width = int(line[0])
                self.height = int(line[1])
               
            #read blocked cells
                blocked = dict()
                for line in f.readlines():
                    half = line.strip().split()
                    # blocked (vertex,0 or 1 blocked)
                    blocked[(int(half[0]) - 1, int(half[1]) - 1)] = int(half[2])
                
                self.start_graph(blocked)

        def start_graph(self, blocked):
            for x in range(self.width + 1):
                row = []
                for y in range(self.height + 1):
                    if x == self.width or y == self.height:
                        b = 1
                    else:
                        b = blocked[(x,y)]
                    row.append(Node(x, y, b))
                self.nodes.append(row)
        #construct edges for the graph (p1,p2)
            for x in range(self.width + 1):
                for y in range(self.height + 1):
                    if x > 0 and y > 0 and self.nodes[x-1][y-1].blocked == 0:
                     self.edges[((x,y),(x-1,y-1))] = Edge((x,y), (x-1,y-1), math.sqrt(2))

                    if x < self.width and y > 0 and self.nodes[x][y-1].blocked == 0:
                     self.edges[((x,y),(x+1, y-1))] = Edge((x,y), (x+1, y-1), math.sqrt(2))
                
                    if y > 0:
                        if x == 0 and self.nodes[x][y-1].blocked == 0:
                            self.edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)
                        elif x > 0 and (self.nodes[x-1][y-1].blocked == 0 or self.nodes[x][y-1].blocked == 0):
                            self.edges[((x,y),(x, y-1))] = Edge((x,y), (x, y-1), 1)

                    if x < self.width:
                        if y == 0 and self.nodes[x][y].blocked == 0:
                            self.edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)
                        elif y > 0 and (self.nodes[x][y-1].blocked == 0 or self.nodes[x][y].blocked == 0):
                            self.edges[((x,y),(x+1, y))] = Edge((x,y), (x+1, y), 1)

def line_of_sight(self, s, e, nodes): 
        x0 = s.x
        y0 = s.y
        x1 = e.x
        y1 = e.y
        f = 0
        dy = y1 - y0
        dx = x1 - x0

        if dy < 0:
            dy = -dy
            sy = -1
        else:
            sy = 1

        if dx < 0:
            dx = -dx
            sx = -1
        else:
            sx = 1

        if dx >= dy:
            while x0 != x1:
                f += dy
                if f >= dx:
                    if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                        return False
                    y0 += sy
                    f -= dx
                if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                    return False
                if dy == 0 and nodes[x0 + ((sx - 1)//2)][y0].blocked and nodes[x0 + ((sx - 1)//2)][y0 - 1].blocked:
                    return False
                x0 += sx
        else:
            while y0 != y1:
                f += dx
                if f >= dy:
                    if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1 )//2)].blocked:
                        return False
                    x0 += sx
                    f -= dy

                if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                    return False
                if dx == 0 and nodes[x0][y0 + ((sy - 1)//2)].blocked and nodes[x0 - 1][y0 + ((sy - 1)//2)].blocked:
                    return False
                y0 += sy
        return True
#returns the visible edges for theta* 
def vis_graph(self):
        
        if self.vis_edges:
            return self.vis_edges

        self.vnodes = []
        self.vis_edges = dict()
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if (i == self.src[0] and j == self.src[1]) or (i == self.dst[0] and j == self.dst[1]):
                    self.vnodes.append(self.nodes[i][j])
                elif self.nodes[i][j].blocked == 1:
                    if i == len(self.nodes) - 1 or j == len(self.nodes[i]) - 1:
                        continue
                    self.vnodes.extend([self.nodes[i][j], self.nodes[i+1][j], self.nodes[i][j+1], self.nodes[i+1][j+1]])

        for vnode in self.vnodes:
            for vis in self.vnodes:
                if vis == vnode:
                    continue
                if self.line_of_sight(vnode, vis, self.nodes):
                    self.vis_edges[((vnode.x, vnode.y), (vis.x, vis.y))] = Edge((vnode.x, vnode.y), (vis.x, vis.y), 1)

        return self.vis_edges