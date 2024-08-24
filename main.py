from window import *
from cell import*


def main():
    win = Window(800, 600)
    row = []
    collum = []
    for i in range(2, 8):
        row.append(Cell(win, i*50, i*50+50, 100, 150))
    for i in range(len(row)):
        row[i].draw("blue")



    win.wait_for_close()


main()