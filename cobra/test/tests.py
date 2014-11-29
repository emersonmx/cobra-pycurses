import time
import curses

def window_test(stdscr):
    curses.use_default_colors()
    curses.start_color()
    stdscr.border()

    nw = stdscr.subwin(10, 20, 5, 10)
    nw.border()

    while 1:
        k = stdscr.getch()
        if k == ord('q'):
            break
        elif k == ord('p'):
            nw.addstr("Hello")

        stdscr.noutrefresh()
        nw.noutrefresh()
        curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(window_test)
