import heapq
import random
import time
from math import *
from tkinter import *
import numpy as np


class CreateGrid:
    def __init__(self, grid_length, grid_height):
        self.grid_length = grid_length
        self.grid_height = grid_height
        list_x = random.sample(range(1, grid_length + 2), 2)
        list_y = random.sample(range(1, grid_height + 2), 2)

        file = open('grid.txt', 'w')
        file.write(str(list_x[0]) + ' ' + str(list_y[0]) + '\n')
        file.write(str(list_x[1]) + ' ' + str(list_y[1]) + '\n')
        file.write(str(grid_length) + ' ' + str(grid_height) + '\n')

        num_blocked_tiles = ceil(0.1 * grid_length * grid_height)

        for i in range(1, grid_length + 1):
            for j in range(1, grid_height + 1):
                x = random.randint(1, grid_length * grid_height)
                if x <= num_blocked_tiles:
                    file.write(str(i) + ' ' + str(j) + ' ' + '1' + '\n')
                else:
                    file.write(str(i) + ' ' + str(j) + ' ' + '0' + '\n')

        file.close()


class LoadGrid:
    def __init__(self, filename):
        self.filename = filename
        self.window = Tk()
        self.window.geometry("1000x1000")

        self.frame = Frame(self.window, width=300, height=300)
        self.frame.pack(expand=True, fill=BOTH)

        self.blocked = [[]]

        self.canvas = Canvas(self.frame)

        def do_zoom(event):
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            factor = 1.01 ** event.delta
            self.canvas.scale(ALL, x, y, factor, factor)

        self.canvas.bind("<MouseWheel>", do_zoom)
        self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
        self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))

        with open(self.filename) as file:
            self.start_x, self.start_y = [int(x) for x in next(file).split()]
            self.goal_x, self.goal_y = [int(x) for x in next(file).split()]
            self.grid_length, self.grid_height = [int(x) for x in next(file).split()]

            print(f"grid length: {self.grid_length} grid height: {self.grid_height}")

            self.canvas.config(width=(self.grid_length * 50) + 100, height=(self.grid_height * 50) + 100)

            a, b, c, d = 5, 5, 55, 55

            for i in range(1, self.grid_length + 1):
                for j in range(1, self.grid_height + 1):
                    _, _, s = [int(x) for x in next(file).split()]
                    if s == 0:
                        self.canvas.create_rectangle(a, b, c, d)
                        self.blocked[i - 1].append(False)
                    else:
                        self.canvas.create_rectangle(a, b, c, d, fill="black")
                        self.blocked[i - 1].append(True)

                    b += 50
                    d += 50
                self.blocked.append([])
                b = 5
                d = 55
                a += 50
                c += 50
            self.blocked.remove(self.blocked[-1])

        self.canvas.create_oval(0 + (50 * (self.start_x - 1)), 0 + (50 * (self.start_y - 1)),
                                10 + (50 * (self.start_x - 1)),
                                10 + (50 * (self.start_y - 1)), fill="red")

        self.canvas.create_oval(0 + (50 * (self.goal_x - 1)), 0 + (50 * (self.goal_y - 1)),
                                10 + (50 * (self.goal_x - 1)),
                                10 + (50 * (self.goal_y - 1)), fill="blue")

        # astar_button = Button(self.window, text="A*", command=main, height=2, width=10)
        # astar_button.place(relx=2, rely=2, anchor=CENTER)
        # astar_button.pack()
        #
        # thetastar_button = Button(self.window, text="Theta*", command=main, height=2, width=10).pack()

        # self.canvas.pack(padx=10, pady=10, expand=True)
        # self.window.mainloop()


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = float('inf')
        self.parent = None

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        return 1

    def equals(self, other):
        return self.x == other.x and self.y == other.y

    def heuristic(self, goal):
        self.h = sqrt(2) * min(abs(self.x - goal.x), abs(self.y - goal.y)) + \
                 max(abs(self.x - goal.x), abs(self.y - goal.y)) - \
                 min(abs(self.x - goal.x), abs(self.y - goal.y))

        return self.h

    def f(self, goal):
        return self.g + self.heuristic(goal)


def find_astar(grid):
    start = Node(grid.start_x, grid.start_y)
    goal = Node(grid.goal_x, grid.goal_y)
    # goal = Node(grid.start_x, grid.start_y)
    print(f"start: {start}")
    print(f"goal: {goal}")
    # print(start, goal)
    start.g = 0
    start.parent = start
    fringe = []
    heapq.heappush(fringe, (start, start.f(goal)))

    closed = []
    while fringe:
        (s, f) = heapq.heappop(fringe)
        if s.x == goal.x and s.y == goal.y:
            print("path found")

            # print(s.parent)
            grid.canvas.create_line(5 + (s.x - 1) * 50, 5 + (s.y - 1) * 50, 5 + (s.parent.x - 1) * 50,
                                    5 + (s.parent.y - 1) * 50,
                                    width=5, fill="green")
            current_node = s.parent
            print(s)
            print(current_node)
            while not (current_node.equals(start)):
                grid.canvas.create_line(5 + (current_node.x - 1) * 50, 5 + (current_node.y - 1) * 50,
                                        5 + (current_node.parent.x - 1) * 50, 5 + (current_node.parent.y - 1) * 50,
                                        width=5, fill="green")
                print(current_node.parent)
                current_node = current_node.parent

            grid.canvas.pack(padx=10, pady=10, expand=True)
            grid.window.mainloop()

            # print(grid.blocked[0][2])

            return
        # print(s, f)
        closed.append(s)

        # child_list = children(s, grid.grid_length, grid.grid_height)

        for child in children(s, grid.grid_length, grid.grid_height):
            # print(f"child: {child}")
            in_closed = False
            in_fringe = False
            for x in closed:
                if child.equals(x):
                    in_closed = True
            for (y, z) in fringe:
                if child.equals(y):
                    in_fringe: True
            if not in_closed:
                if not in_fringe:
                    print("*******")
                    child.g = float('inf')
                    child.parent = None
                update_vertex_astar(s, child, fringe, goal, grid.blocked, closed)
                # print(line_of_sight(Node(4,2), Node(3,4), grid.blocked))

    print("no path found")
    grid.canvas.pack(padx=10, pady=10, expand=True)
    grid.window.mainloop()
    return


def update_vertex_astar(s, child, fringe, goal, blocked, closed):
    dx = s.x - child.x
    dy = s.y - child.y
    d = sqrt(dx ** 2 + dy ** 2)
    # print(s)
    # print(child)
    print("fringe:")
    for (a, b) in fringe:
        print(a, round(b, 2))
    print()
    print("closed")
    for n in closed:
        print(n)
    print("---------------------------")

    if s.g + d <= child.g and line_of_sight(s, child, blocked):
        child.g = s.g + d
        child.parent = s
        for (a, b) in fringe:
            if child.equals(a):
                fringe.remove((a, b))
        heapq.heapify(fringe)
        heapq.heappush(fringe, (child, child.f(goal)))


def find_theta_star(grid):
    start = Node(grid.start_x, grid.start_y)
    goal = Node(grid.goal_x, grid.goal_y)
    # goal = Node(grid.start_x, grid.start_y)
    print(f"start: {start}")
    print(f"goal: {goal}")
    # print(start, goal)
    start.g = 0
    start.parent = start
    fringe = []
    heapq.heappush(fringe, (start, start.f(goal)))

    closed = []
    while fringe:
        (s, f) = heapq.heappop(fringe)
        if s.x == goal.x and s.y == goal.y:
            print("path found")

            # print(s.parent)
            grid.canvas.create_line(5 + (s.x - 1) * 50, 5 + (s.y - 1) * 50, 5 + (s.parent.x - 1) * 50,
                                    5 + (s.parent.y - 1) * 50,
                                    width=5, fill="green")
            current_node = s.parent
            print(s)
            print(current_node)
            while not (current_node.equals(start)):
                grid.canvas.create_line(5 + (current_node.x - 1) * 50, 5 + (current_node.y - 1) * 50,
                                        5 + (current_node.parent.x - 1) * 50, 5 + (current_node.parent.y - 1) * 50,
                                        width=5, fill="green")
                print(current_node.parent)
                current_node = current_node.parent

            grid.canvas.pack(padx=10, pady=10, expand=True)
            grid.window.mainloop()

            # print(grid.blocked[0][2])

            return
        # print(s, f)
        closed.append(s)

        # child_list = children(s, grid.grid_length, grid.grid_height)

        for child in children(s, grid.grid_length, grid.grid_height):
            # print(f"child: {child}")
            in_closed = False
            in_fringe = False
            for x in closed:
                if child.equals(x):
                    in_closed = True
            for (y, z) in fringe:
                if child.equals(y):
                    in_fringe: True
            if not in_closed:
                if not in_fringe:
                    # print("*******")
                    child.g = float('inf')
                    child.parent = None
                update_vertex_theta_star(s, child, fringe, goal, grid.blocked, closed)
                # print(line_of_sight(Node(3, 6), Node(3, 5), grid.blocked))
                # print(line_of_sight(Node(4,2), Node(3,4), grid.blocked))

    print("no path found")
    grid.canvas.pack(padx=10, pady=10, expand=True)
    grid.window.mainloop()
    return


def update_vertex_theta_star(s, child, fringe, goal, blocked, closed):
    # print(s)
    # print(child)
    # print("fringe:")
    # for (a, b) in fringe:
    #     print(a, round(b, 2))
    # print()
    # print("closed")
    # for n in closed:
    #     print(n)
    # print("---------------------------")

    if line_of_sight(s.parent, child, blocked):
        if s.parent.g + distance(s.parent, child) < child.g:
            child.g = s.parent.g + distance(s.parent, child)
            child.parent = s.parent
            for (a, b) in fringe:
                if child.equals(a):
                    fringe.remove((a, b))
            heapq.heappush(fringe, (child, child.f(goal)))

    else:
        if s.g + distance(s, child) < child.g:
            child.g = s.g + distance(s, child)
            child.parent = s
            for (a, b) in fringe:
                if child.equals(a):
                    fringe.remove((a, b))
            heapq.heapify(fringe)
            heapq.heappush(fringe, (child, child.f(goal)))


def distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return sqrt(dx ** 2 + dy ** 2)


def line_of_sight(s, child, blocked):
    x0 = s.x
    y0 = s.y
    x1 = child.x
    y1 = child.y
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
    # try:
    if dx >= dy:
        while x0 != x1:
            # print(
            #     f"x0, y0: {x0, y0}, sx, sy:{sx, sy}, blocked[0]: {len(blocked[0])}, blocked: {len(blocked)}, {blocked}\n")
            f = f + dy
            # if y0 > len(blocked[0]) + 1 or x0 > len(blocked) + 1 or y0 < 1 or x0 < 1:
            #     return False
            # print(x0 + int((sx - 1) / 2) - 1, y0 + int((sy - 1) / 2) - 1)
            # print(x0 + int((sx - 1) / 2) - 1, y0 - 1)
            # print(x0 + int((sx - 1) / 2) - 1, y0 - 2)
            try:
                if f >= dx:
                    if blocked[x0 + int((sx - 1) / 2) - 1][y0 + int((sy - 1) / 2) - 1]:
                        return False
                    y0 = y0 + sy
                    f = f - dx
                if f != 0 and blocked[x0 + int((sx - 1) / 2) - 1][y0 + int((sy - 1) / 2) - 1]:
                    return False
                if dy == 0 and blocked[x0 + int((sx - 1) / 2) - 1][y0 - 1] and blocked[x0 + int((sx - 1) / 2) - 1][y0 - 2]:
                    return False
                x0 = x0 + sx
            except IndexError:
                # print("ERRORRRRRRRRRRRRRRR")
                return False

    else:

        while y0 != y1:
            # print(
            #     f"x0, y0: {x0, y0}, sx, sy:{sx, sy}, blocked[0]: {len(blocked[0])}, blocked: {len(blocked)}, {blocked}\n")
            f = f + dx
            # if y0 > len(blocked[0]) + 1 or x0 > len(blocked) + 1 or y0 < 1 or x0 < 1:
            #     return False
            # print(x0 + int((sx - 1) / 2) - 1, y0 + int((sy - 1) / 2) - 1)
            # print(x0 - 1, y0 + int((sy - 1) / 2) - 1)
            # print()
            try:
                if f >= dy:
                    if blocked[x0 + int((sx - 1) / 2) - 1][y0 + int((sy - 1) / 2) - 1]:
                        return False
                    x0 = x0 + sx
                    f = f - dy
                if f != 0 and blocked[x0 + int((sx - 1) / 2) - 1][y0 + int((sy - 1) / 2) - 1]:
                    return False

                if dx == 0 and blocked[x0 - 1][y0 + int((sy - 1) / 2) - 1] and blocked[x0 - 2][y0 + int((sy - 1) / 2) - 1]:
                    return False
                y0 = y0 + sy
            except IndexError:
                # print("ERRORRRRRRRRRRRRRRR")
                return False
    # except IndexError:
    #     return False

    return True


def children(s, length, height):
    c1 = [Node(s.x + 1, s.y), Node(s.x, s.y + 1), Node(s.x + 1, s.y + 1), Node(s.x - 1, s.y), Node(s.x, s.y - 1),
          Node(s.x + 1, s.y - 1), Node(s.x - 1, s.y + 1), Node(s.x - 1, s.y - 1)]
    c2 = []

    for i in range(0, len(c1)):
        if (c1[i].x in range(1, length + 2)) and (c1[i].y in range(1, height + 2)):
            # print(f"nx, ny: {n.x,n.y}")
            c2.append(c1[i])
    return c2


def main():
    options = ["Create Grid", "Find A*", "Find Theta*"]

    for i in range(len(options)):
        print(f"{i + 1}: {options[i]}")

    inp = int(input("Enter a number: "))

    if inp in range(1, 5):
        if inp == 1:
            length, height = map(int, input("Enter the length and height of the grid: ").split())
            grid = CreateGrid(length, height)

        elif inp == 2:
            grid = LoadGrid(filename=input("Enter the name of the file: "))
            # grid = LoadGrid(filename="grid.txt")
            find_astar(grid)
        elif inp == 3:
            grid = LoadGrid(filename=input("Enter the name of the file: "))
            # grid = LoadGrid(filename="grid.txt")
            find_theta_star(grid)
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
