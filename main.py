from window import *
#from maze_recursion import*
from maze_stack import*
# import only one or the other at one time
# they have the same Maze class name



def main():
    win = Window(1600, 800)
    maze = Maze(100, 100, 30, 30, 20, win)



    win.wait_for_close()


main()