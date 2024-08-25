from window import*
import time
import random


class Cell:
    def __init__(self, x1, x2,y1, y2, win = None):
        self.__center = Point((x1+x2)/2, (y1+y2)/2)
        self.__walls = { "right": [Line(Point(x2, y1), Point(x2, y2)), True],
                        "bottom": [Line(Point(x1, y2), Point(x2, y2)), True],
                        "top": [Line(Point(x1, y1), Point(x2, y1)), True],
                        "left": [Line(Point(x1, y1), Point(x1, y2)), True]
                        }
        self.right = None
        self.left = None
        self.top = None
        self.bottom = None
        self.win = win
        self.exit = False
        self.visited = False

    def set_wall(self, wall):
        self.__walls[wall][1] = True

    def delete_wall(self, wall):
        self.__walls[wall][1] = False
        self.draw()

    def draw(self, color = "black"):
        for wall in self.__walls.keys():
            if self.__walls[wall][1]:
                self.win.draw(self.__walls[wall][0], color)
            else:
                self.win.draw(self.__walls[wall][0], "white")

    def draw_move(self, to_cell, undo=False):
        line = Line(self.__center, to_cell.__center)
        if undo:
            self.win.draw(line, "red")
        else:
            self.win.draw(line, "blue")

    def __repr__(self):
        return f'{self.__walls["top"]}, {self.__walls["right"]}, {self.__walls["bottom"]}, {self.__walls["left"]}'


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size,
        win = None,
    ):
        self.__x = x1
        self.__y = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size = cell_size
        self.win = win
        self.__found_exit = False
        self.__stack = []
        self.__create_cells()

    def __create_cells(self):
        cells = []
        for j in range(0, self.__num_rows):
            row = []
            for i in range(0, self.__num_cols):
                row.append(Cell(i*self.__cell_size + self.__x,
                                i*self.__cell_size + self.__x + self.__cell_size,
                                j*self.__cell_size + self.__y,
                                j*self.__cell_size + self.__y + self.__cell_size,
                                self.win
                                ))
                row[-1].draw()
            cells.append(row)
        self.__stack.append(cells[0][0])
        print(self.__stack)
        self.__create_graph(cells)
        self.__break_entrance_and_exit()
        self.__break_walls_s()
        self.__reset_visited(cells)

    def __create_graph(self, cells):
        for j in range(0, self.__num_rows):
            for i in range(0, self.__num_cols):
                current = cells[i][j]
                if i-1 in range(0, self.__num_rows) and j in range(0, self.__num_cols):
                    current.top = cells[i-1][j]

                if i+1 in range(0, self.__num_rows) and j in range(0, self.__num_cols):
                    current.bottom = cells[i+1][j]

                if i in range(0, self.__num_rows) and j-1 in range(0, self.__num_cols):
                    current.left = cells[i][j-1]

                if i in range(0, self.__num_rows) and j+1 in range(0, self.__num_cols):
                    current.right = cells[i][j+1]

    def __animate(self):
        self.win.redraw()
        #time.sleep(0.05)

    def __break_entrance_and_exit(self):
        temp = self.__stack[0]
        temp.delete_wall("top")
        for i in range(self.__num_rows-1):
            temp = temp.bottom
        for i in range(self.__num_cols-1):
            temp = temp.right
        temp.delete_wall("bottom")
        temp.exit = True

    #for maze generation
    def __break_walls_s(self):
        while len(self.__stack) != 0:
            self.__stack[-1].visited = True
                
            possible_next = self.__add_unvisited_neighbors(self.__stack[-1])
            if possible_next is None:
                self.__stack.pop()
            else:
                self.__move_to_next(possible_next)

    #for maze generation
    def __add_unvisited_neighbors(self, current):
        possible_next = []
        if current.top is not None and not current.top.visited:
            possible_next.append("top")

        if current.bottom is not None and not current.bottom.visited:
            possible_next.append("bottom")

        if current.left is not None and not current.left.visited:
            possible_next.append("left")

        if current.right is not None and not current.right.visited:
            possible_next.append("right")
        
        if len(possible_next) == 0:
            return None
        return possible_next

    #for maze generation 
    def __move_to_next(self, possible_next):
            match(possible_next[random.randrange(0, len(possible_next))]):
                case("top"):
                    self.__stack[-1].delete_wall("top")
                    self.__stack[-1].top.delete_wall("bottom")
                    self.__animate()
                    self.__stack.append(self.__stack[-1].top)

                case("bottom"):
                    self.__stack[-1].delete_wall("bottom")
                    self.__stack[-1].bottom.delete_wall("top")
                    self.__animate()
                    self.__stack.append(self.__stack[-1].bottom)

                case("left"):
                    self.__stack[-1].delete_wall("left")
                    self.__stack[-1].left.delete_wall("right")
                    self.__animate()
                    self.__stack.append(self.__stack[-1].left)

                case("right"):
                    self.__stack[-1].delete_wall("right")
                    self.__stack[-1].right.delete_wall("left")
                    self.__animate()
                    self.__stack.append(self.__stack[-1].right)

                case _:
                    raise Exception("Problem in Maze/__break_walls_r")
        
    #reset visited
    def __reset_visited(self, cells):      
        for i in range(0, self.__num_rows):
            for j in range(0, self.__num_cols):
                cells[i][j].visited = False

    