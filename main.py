from window import *
from cell import*


def main():
    win = Window(1600, 800)
    maze = Maze(100, 100, 30, 70, 20, win)
    maze.reset_try()    
    maze.solve_r()



    win.wait_for_close()


main()