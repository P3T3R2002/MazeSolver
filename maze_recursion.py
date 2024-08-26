from window import*
#import time
import random


class Cell:
    def __init__(self, x1, x2,y1, y2, win = None):
        self.center = Point((x1+x2)/2, (y1+y2)/2)
        self.walls = { "right": [Line(Point(x2, y1), Point(x2, y2)), True],
                        "bottom": [Line(Point(x1, y2), Point(x2, y2)), True],
                        "top": [Line(Point(x1, y1), Point(x2, y1)), True],
                        "left": [Line(Point(x1, y1), Point(x1, y2)), True]
                        }
        self.win = win
        self.visited = False
    
    def set_wall(self, wall):
        self.walls[wall][1] = True

    def delete_wall(self, wall):
        self.walls[wall][1] = False

    def draw(self, color = "black"):
        for wall in self.walls.keys():
            if self.walls[wall][1]:
                self.win.draw(self.walls[wall][0], color)
            else:
                self.win.draw(self.walls[wall][0], "white")

    def draw_move(self, to_cell, undo=False):
        line = Line(self.center, to_cell.center)
        if undo:
            self.win.draw(line, "red")
        else:
            self.win.draw(line, "blue")

    def __repr__(self):
        return f'{self.walls["top"]}, {self.walls["right"]}, {self.walls["bottom"]}, {self.walls["left"]}'


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
        self.__cells = []
        self.win = win
        self.__found_exit = False
        self.__create_cells()
        self.current = None

    def __create_cells(self):
        for j in range(0, self.__num_rows):
            row = []
            for i in range(0, self.__num_cols):
                row.append(Cell(i*self.__cell_size + self.__x,
                                i*self.__cell_size + self.__x + self.__cell_size,
                                j*self.__cell_size + self.__y,
                                j*self.__cell_size + self.__y + self.__cell_size,
                                self.win
                                ))
            self.__cells.append(row)
        self.__draw_cell()
        self.__reset_try()

    def __draw_cell(self):
        for row in self.__cells:
            for cell in row:
                cell.draw()
                self.__animate()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)

    def __animate(self):
        self.win.redraw()
        #time.sleep(0.01)

    def __break_entrance_and_exit(self):
        self.__break_wall(self.__cells[0][0], "top")
        self.__break_wall(self.__cells[-1][-1], "bottom")

    def __break_wall(self, wall, direction):
        wall.delete_wall(direction)
        wall.draw()

    #for maze generation
    def __break_walls_r(self, i, j, to_visit = []):
        current = self.__cells[i][j]
        current.visited = True
        possible_next = self.__add_unvisited_neighbors(i, j, to_visit)
        while possible_next is not None:
            next_direction = self.__get_next_direction(possible_next)
            match(next_direction):
                case("top"):
                    self.__break_wall(self.__cells[i][j], "top")
                    self.__break_wall(self.__cells[i-1][j], "bottom")
                    self.__animate()
                    self.__break_walls_r(i-1, j, to_visit)

                case("bottom"):
                    self.__break_wall(self.__cells[i][j], "bottom")
                    self.__break_wall(self.__cells[i+1][j], "top")
                    self.__animate()
                    self.__break_walls_r(i+1, j, to_visit)

                case("left"):
                    self.__break_wall(self.__cells[i][j], "left")
                    self.__break_wall(self.__cells[i][j-1], "right")
                    self.__animate()
                    self.__break_walls_r(i, j-1, to_visit)

                case("right"):
                    self.__break_wall(self.__cells[i][j], "right")
                    self.__break_wall(self.__cells[i][j+1], "left")
                    self.__animate()
                    self.__break_walls_r(i, j+1, to_visit)

                case _:
                    raise Exception("Problem in Maze/__break_walls_r")
                
            possible_next = self.__add_unvisited_neighbors(i, j, to_visit)

    #for maze generation
    def __add_unvisited_neighbors(self, i, j, to_visit):
        possible_next = []
        if i-1 in range(0, self.__num_rows) and j in range(0, self.__num_cols) and not self.__cells[i-1][j].visited:
            to_visit.append((i-1, j))
            possible_next.append("top")

        if i+1 in range(0, self.__num_rows) and j in range(0, self.__num_cols) and not self.__cells[i+1][j].visited:
            to_visit.append((i+1, j))
            possible_next.append("bottom")

        if i in range(0, self.__num_rows) and j-1 in range(0, self.__num_cols) and not self.__cells[i][j-1].visited:
            to_visit.append((i, j-1))
            possible_next.append("left")

        if i in range(0, self.__num_rows) and j+1 in range(0, self.__num_cols) and not self.__cells[i][j+1].visited:
            to_visit.append((i, j+1))
            possible_next.append("right")
        
        if len(possible_next) == 0:
            return None
        return possible_next

    #for maze generation 
    def __get_next_direction(self, possible_next):
        return possible_next[random.randrange(0, len(possible_next))]
    
    #for maze solving
    def __add_possible_routes(self, i, j, to_visit):
        if i == self.__num_rows-1 and j == self.__num_cols-1:
            return None
        possible_next = []
        for direction in self.__cells[i][j].walls.keys():
            current = self.__cells[i][j]
            match(direction):
                case("top"):
                    if not current.walls[direction][1] and not self.__cells[i-1][j].visited:
                        to_visit.append((i-1, j))
                        possible_next.append("top")

                case("bottom"):
                    if not current.walls[direction][1] and not self.__cells[i+1][j].visited:
                        to_visit.append((i+1, j))
                        possible_next.append("bottom")

                case("left"):
                    if not current.walls[direction][1] and not self.__cells[i][j-1].visited:
                        to_visit.append((i, j-1))
                        possible_next.append("left")

                case("right"):
                    if not current.walls[direction][1] and not self.__cells[i][j+1].visited:
                        to_visit.append((i, j+1))
                        possible_next.append("right")

                case _:
                    raise Exception("Problem in Maze/__add_possible_routes")
                
        if len(possible_next) == 0:
            return None
        return possible_next

    #for maze solving
    def __get_next_route(self, possible_next):
        return possible_next[0]

    #for recursive maze solving
    def __solve_r(self, i = 0, j = 0, to_visit = []):
        if self.__num_cols-1 == j and self.__num_rows-1 == i:
            self.__found_exit = True
        current = self.__cells[i][j]
        current.visited = True
        possible_next = self.__add_possible_routes(i, j, to_visit)
        while possible_next is not None:
            if self.__found_exit:
                break
            next_direction = self.__get_next_route(possible_next)
            match(next_direction):
                case("top"):
                    self.__cells[i][j].draw_move(self.__cells[i-1][j])
                    self.__animate()
                    self.__solve_r(i-1, j, to_visit)
                    if not self.__found_exit:
                        self.__cells[i][j].draw_move(self.__cells[i-1][j], True)
                        self.__animate()
                    else:
                        break

                case("bottom"):
                    self.__cells[i][j].draw_move(self.__cells[i+1][j])
                    self.__solve_r(i+1, j, to_visit)
                    if not self.__found_exit:
                        self.__cells[i][j].draw_move(self.__cells[i+1][j], True)
                        self.__animate()
                    else:
                        break

                case("left"):
                    self.__cells[i][j].draw_move(self.__cells[i][j-1])
                    self.__solve_r(i, j-1, to_visit)
                    if not self.__found_exit:
                        self.__cells[i][j].draw_move(self.__cells[i][j-1], True)
                        self.__animate()
                    else:
                        break

                case("right"):
                    self.__cells[i][j].draw_move(self.__cells[i][j+1])
                    self.__solve_r(i, j+1, to_visit)
                    if not self.__found_exit:
                        self.__cells[i][j].draw_move(self.__cells[i][j+1], True)
                        self.__animate()
                    else:
                        break
                case _:
                    raise Exception("Problem in Maze/solve_r")    
            possible_next = self.__add_possible_routes(i, j, to_visit)

    #reset visited
    def __reset_try(self):      
        for i in range(0, self.__num_rows):
            for j in range(0, self.__num_cols):
                self.__cells[i][j].visited = False

    def solve(self):
        self.__solve_r()