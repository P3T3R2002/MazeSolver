from window import *
#from maze_recursion import*
from maze_stack import*
# import only one or the other at one time
# they have the same Maze class name



def main():
    win = Window(1800, 1000)
    maze = Maze(100, 50, 80, 160, 10, win)
    maze.solve()


    win.wait_for_close()


main()