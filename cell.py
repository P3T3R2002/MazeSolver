from window import*


class Cell:
    def __init__(self, win, x1, x2,y1, y2):
        self.center = Point((x1+x2)/2, (y1+y2)/2)
        self.walls = {  "top": [Line(Point(x1, y1), Point(x2, y1)), True],
                        "right": [Line(Point(x2, y1), Point(x2, y2)), True],
                        "bottom": [Line(Point(x1, y2), Point(x2, y2)), True],
                        "left": [Line(Point(x1, y1), Point(x1, y2)), True]
                        }
        self.win = win
    
    def set_wall(self, wall):
        self.walls[wall][1] = True

    def delete_wall(self, wall):
        self.walls[wall][1] = False

    def draw(self, color = "black"):
        for wall in self.walls.keys():
            if self.walls[wall][1]:
                self.win.draw(self.walls[wall][0], color)

    def draw_move(self, to_cell, undo=False):
        line = Line(self.center, to_cell.center)
        if undo:
            self.win.draw(line, "grey")
        else:
            self.win.draw(line, "red")

