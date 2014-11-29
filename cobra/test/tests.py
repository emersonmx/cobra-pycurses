import time
import curses

def window_test(stdscr):
    curses.use_default_colors()
    curses.start_color()
    curses.resizeterm(24, 80)

    nw = stdscr.subwin(1, 0)
    nw.border()
    nw2 = nw.derwin(1, 1)
    nw2.border()
    stdscr.addstr(0, 0, "Score: 10923")

    while 1:
        k = stdscr.getch()
        if k == ord('q'):
            break
        elif k == ord('p'):
            nw.addstr("Hello")

        stdscr.noutrefresh()
        nw.noutrefresh()
        nw2.noutrefresh()
        curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(window_test)
