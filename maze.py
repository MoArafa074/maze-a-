import tkinter as tk
import heapq
import random

class Node:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float('inf')  # distance from start node
        self.h = float('inf')  # heuristic distance to end node
        self.f = float('inf')  # total cost
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def generate_maze(rows, cols, density):
    maze = [[Node(x, y, random.random() < density) for y in range(cols)] for x in range(rows)]  # between 0 and 1.
    maze[0][0].is_wall = False  # start node
    maze[rows-1][cols-1].is_wall = False  # end node
    return maze

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

#getting a node's neigbour

def get_neighbors(node, maze):
    neighbors = []
    rows = len(maze)
    cols = len(maze[0])
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, down, left, up

#Checking Validity of Neighbors:

    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and not maze[nx][ny].is_wall:  
            neighbors.append(maze[nx][ny])

    return neighbors

def reconstruct_path(current):

    #Traversing Backwards: follows the parent pointers from the current node to its parent,
    #  then from the parent to its parent, and so on, until it reaches the start node
    path = []
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent
    return path[::-1]

def astar(maze):
    rows = len(maze)
    cols = len(maze[0])
    start = maze[0][0]        #defining the start node and end node
    end = maze[4][4]

    open_set = []
    heapq.heappush(open_set, start) #pushing the start node and empty list "open_set"

    start.g = 0 # is set to 0 because it's the distance from the start node (which is the start node itself).

    start.h = heuristic(start, end) #calculating the huristic of start

    start.f = start.g + start.h 

    while open_set:  #The open_set typically contains nodes that have been discovered but not yet explored.
        current = heapq.heappop(open_set)    #This line pops the node with the lowest f value from the open_set
        if current == end: 
            return reconstruct_path(current) 
        
        for neighbor in get_neighbors(current, maze):
            tentative_g = current.g + 1  # This calculates the tentative cost (g)

            if tentative_g < neighbor.g: #: This condition checks if the newly calculated g value 
                                          #for the neighbor is less than its current g
                
              
                neighbor.parent = current  #If the tentative path to the neighbor is better than before,
                                           #the parent of the neighbor is updated to be the current node.
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

    return None   #If the open_set becomes empty without finding the goal node, 

                   #it means there's no path from the start node to the goal node.

def draw_maze(canvas, maze):
    rows = len(maze)
    cols = len(maze[0])
    cell_width = 20
    cell_height = 20

    for x in range(rows):
        for y in range(cols):
            color = "black" if maze[x][y].is_wall else "white"
            canvas.create_rectangle(y * cell_width, x * cell_height,
                                    (y + 1) * cell_width, (x + 1) * cell_height,
                                    fill=color, outline="")

def draw_path(canvas, path):
    cell_width = 20
    cell_height = 20
    for x, y in path:
        canvas.create_rectangle(y * cell_width, x * cell_height,
                                (y + 1) * cell_width, (x + 1) * cell_height,
                                fill="yellow", outline="")

def solve_maze():
    maze = generate_maze(20, 20, 0.3)
    path = astar(maze)
    if path:
        draw_path(canvas, path)

root = tk.Tk()
root.title("A* Maze Solver")

canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

draw_maze(canvas, generate_maze(20, 20, 0.3))

solve_button = tk.Button(root, text="Solve", command=solve_maze)
solve_button.pack()

root.mainloop()
