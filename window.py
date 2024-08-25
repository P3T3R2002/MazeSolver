from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze"
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root, width=width, height=height, background = "white")
        self.__canvas.pack(fill="both", expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def __close(self):
        self.__running = False

    def draw(self, line, color):
        line.draw(self.__canvas, color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"{self.x}:{self.y}"


class Line:
    def __init__(self, first, second) -> None:
        self.point_1 = first
        self.point_2 = second
    
    def draw(self, canvas, color):
        canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=color, width=2)

    def __repr__(self) -> str:
        return f"{self.point_1} -> {self.point_2}"

