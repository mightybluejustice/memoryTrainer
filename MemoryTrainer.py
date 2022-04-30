import pandas as pd
from mFiles.Mfuncs import *
import curses
from curses import wrapper





if __name__ ==  '__main__':
    NUMSDICT = getItemDict()
    OBJECTLIST = getObjects()
    fail = False

    def main(stdscr):
        curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_BLACK)
        GREENTXT = curses.color_pair(1)
        REDTXT = curses.color_pair(2)
        BLUETXT = curses.color_pair(3)
        printError = False

        while True:
            printMenu(curses, stdscr, printError)
            printError = False
            keypress = stdscr.getch()
            if keypress == ord('1'):
                practiceObjectList(curses, stdscr, NUMSDICT)
            elif keypress == ord('2'):
                memoryNumbers(curses, stdscr, NUMSDICT)
            elif keypress == ord('3'):
                memoryObjects(curses, stdscr, NUMSDICT)                
            elif keypress == ord('4'):
                randomObjects(curses,stdscr, OBJECTLIST)                
            elif keypress == ord('5'):
                randomNumbers(curses,stdscr, OBJECTLIST)                
            elif keypress == ord('6'):
                listObjects(curses, stdscr, OBJECTLIST)                
            elif keypress == ord('7'):
                createAndMemorizeList(curses, stdscr)
            elif keypress == 27:
                break
            else:
                printError = True



    wrapper(main)