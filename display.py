import tkinter as tk
import astar
import thetastar
import time 

class display():
    show_delay = 10
    def __init__(self,x,y):
        self.delay = 0
        self.x = x
        self.y = y
        self.root = tk.Tk()
        self.c = None
        self.WIDTH = 100
        self.HEIGHT = 50
        self.SCALE = 25  # Scale factor for the elements to show properly on the canvas
        self.MIN_SCALE = 25
        self.selected_widget = None
        self.topbar = None
        self.label_x = None
        self.label_y = None
        self.label_g = None
        self.label_h = None
        self.label_f = None
        self.jobs = []
        self.start_window()

    def start_window(self):

        #window setup
        self.root.geometry(str(self.x) + "x" + str(self.y))
        self.root.title("Choose an Algorithm")
        #toolbar
        self.topbar = tk.Frame(self.root, width = self.scale(self.WIDTH), height = 20)
        self.topbar.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        label_cell = tk.Label(self.topbar, text="Selected node: ")
        label_cell.grid(row=0, column=0)
        self.label_x = tk.Label(self.topbar, text="N/A")
        self.label_x.grid(row=0, column=1)
        self.label_y = tk.Label(self.topbar, text="")
        self.label_y.grid(row=0, column=2)
        self.label_g = tk.Label(self.topbar, text="")
        self.label_g.grid(row=0, column=3, padx=(10,0))
        self.label_h = tk.Label(self.topbar, text="")
        self.label_h.grid(row=0, column=4, padx=(10,0))
        self.label_f = tk.Label(self.topbar, text="")
        self.label_f.grid(row=0, column=5, padx=(10,0))

        #Sets up a canvas and scrollbars inside of a frame
        frame = tk.Frame(self.root, width = self.scale(self.WIDTH), height = self.scale(self.HEIGHT))
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.c = tk.Canvas(frame,
                    width = self.scale(self.WIDTH),
                    height = self.scale(self.HEIGHT),
                    borderwidth=0,
                    highlightthickness=0,
                    scrollregion = (0, 0, self.scale(self.WIDTH), self.scale(self.HEIGHT)))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.c.xview)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.c.yview)
        self.c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        menubar = tk.Menu(self.root)
        algorithms_menu = tk.Menu(menubar, tearoff=0)
        algorithms_menu.add_command(label="A*", command=self.__do_a_star)
        algorithms_menu.add_command(label="Theta*", command=self.__do_theta_star)
        menubar.add_cascade(label="Algorithms", menu=algorithms_menu)
        zoom_menu = tk.Menu(menubar, tearoff=0)
        zoom_menu.add_command(label="In", command=lambda: self.zoom(True))
        zoom_menu.add_command(label="Out", command=lambda: self.zoom(False))
        menubar.add_cascade(label="Zoom", menu=zoom_menu)
        self.root.config(menu=menubar)
        self.c.bind("<Button-1>", self.mouse_click)
    
    def reset_grid(self):
        self.c.delete("path")
        self.c.delete(self.selected_widget)
        self.reset_topbar()
        for job in self.jobs:
            self.c.after_cancel(job)
        self.jobs = []
        self.delay = 0

    def reset_topbar(self):
        self.label_x.config(text="N/A")
        self.label_y.config(text="")
        self.label_g.config(text="")
        self.label_h.config(text="")
        self.label_f.config(text="")

       

    def mouse_click(self, event):
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        modx = x % self.SCALE
        mody = y % self.SCALE
        lower_thresh = int(.2 * self.SCALE)
        upper_thresh = self.SCALE - int(.2 * self.SCALE)

        if modx < lower_thresh:
            x = x - modx
        elif modx > upper_thresh:
            x = x + (self.SCALE - modx)
        else:
            return

        if mody < lower_thresh:
            y = y - mody
        elif mody > upper_thresh:
            y = y + (self.SCALE - mody)
        else:
            return

        offset = int(self.SCALE / 5)
        self.c.delete(self.selected_widget)
        self.selected_widget = self.c.create_oval(x - offset,
                      y + offset,
                      x + offset,
                      y - offset,
                      fill='white')

        x = int(x / self.SCALE)
        y = int(y / self.SCALE)

        self.label_x.config(text="(" + str(x + 1) + ",")
        self.label_y.config(text=str(y + 1) + ")")
        self.__set_g(self.graph.nodes[x][y].g)
        self.__set_h(self.graph.nodes[x][y].h)
        self.__set_f(self.graph.nodes[x][y].f)
        x0 = self.c.canvasx(0)
        y0 = self.c.canvasy(0)

    def update_graph(self, graph):
        self.graph = graph
    def __set_g(self, g):
        self.label_g.config(text="g = " + str(g))

    def __set_h(self, h):
        self.label_h.config(text="h = " + str(h))

    def __set_f(self, f):
        self.label_f.config(text="f = " + str(f))

    def __do_a_star(self):
        print("Doing A*")
        self.reset_grid()
        start_time = time.time()
        res = astar.a_star(self, self.graph.src, self.graph.dst, self.graph.nodes, self.graph.edges)
        ti = str(time.time() - start_time)
        print("Time: " + ti + " seconds")
        res.reverse()
        

    def __do_theta_star(self):
        print("Doing Theta*")
        self.reset_grid()
        start_time = time.time()
        res = thetastar.theta_star(self, self.graph.src, self.graph.dst, self.graph.nodes, self.graph.edges)
        ti = str(time.time() - start_time)
        print("time:" + ti + " s")
        res.reverse()
        self.draw_path(res)

    def draw_path(self, path):
        scale = self.scale
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            self.jobs.append(self.c.after(self.delay, self.__draw_line, p1, p2, 'red', 3))
            self.delay += display.show_delay
        self.c.after(self.delay, self.__raise_all)
    def draw_graph(self):

        self.c.delete('edge')
        graph = self.graph
        start = self.graph.src # (93,37)
        end = self.graph.dst  #(22,32)
        
       
        for row in graph.nodes:
            for node in row:
                if node.blocked == 1:
                    self.c.create_rectangle(self.scale(node.x),
                                        self.scale(node.y),
                                        self.scale(node.x + 1),
                                        self.scale(node.y + 1),
                                        fill='gray',
                                        outline='',
                                        tags=("blocked"))

        
        edges = []
        self.graph_type = 0
        edges = list(graph.edges.values())
        
        # Draw the edges
        for edge in edges:
            p1 = edge.p1
            p2 = edge.p2
            self.c.create_line([(self.scale(p1[0]), self.scale(p1[1])), (self.scale(p2[0]), self.scale(p2[1]))], tags=("edge"))

        offset = int(self.SCALE / 5)

        self.c.create_oval(self.scale(start[0]) - offset,
                      self.scale(start[1]) + offset,
                      self.scale(start[0]) + offset,
                      self.scale(start[1]) - offset,
                      fill='green',
                      tag=("endpoint"))

        # Draw the end point
        self.c.create_oval(self.scale(end[0]) - offset,
                      self.scale(end[1]) + offset,
                      self.scale(end[0]) + offset,
                      self.scale(end[1]) - offset,
                      fill='red',
                      tag=("endpoint"))

        self.__raise_all()

    def run(self):
        self.draw_graph()
        self.c.after(self.delay,self.__raise_all)
        self.root.mainloop()

    def scale(self, x):
        return x * self.SCALE
        
    def __raise_all(self):
        self.c.tag_raise('path')
        self.c.tag_raise('endpoint')

    def draw_line(self, p1, p2):
        self.jobs.append(self.c.after(self.delay, self.__draw_line, p1, p2, '#5c9aff', 1.5))
        self.delay += display.show_delay

    def __draw_line(self, p1, p2, fill, width):
        self.c.create_line([(self.scale(p1[0]), self.scale(p1[1])), (self.scale(p2[0]), self.scale(p2[1]))], fill=fill, width=width, tags=("path"))
        if self.scale(p1[0]) < self.c.canvasx(0):
            self.c.xview_moveto((self.c.canvasx(0) - self.SCALE) / self.scale(self.WIDTH))
        if self.scale(p1[1]) < self.c.canvasy(0):
            self.c.yview_moveto((self.c.canvasy(0) - self.SCALE) / self.scale(self.HEIGHT))
        if self.scale(p2[0]) > (self.c.canvasx(0) + self.c.winfo_width()):
            self.c.xview_moveto((self.c.canvasx(0) + self.SCALE) / self.scale(self.WIDTH))
        if self.scale(p2[1]) > (self.c.canvasy(0) + self.c.winfo_height()):
            self.c.yview_moveto((self.c.canvasy(0) + self.SCALE) / self.scale(self.HEIGHT))

   