import time
import curses
import unittest


class TestWindowLayout(unittest.TestCase):

    def test_window(self):
        error_code = 0
        try:
            stdscr = self._test_window_setup_curses()
            self._test_window_run(stdscr)
        except:
            error_code = 1
        finally:
            if "stdscr" in locals():
                self._test_window_dispose_curses(stdscr)

        self.assertEqual(error_code, 0)

    def _test_window_setup_curses(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        try:
            curses.start_color()
        except:
            pass

        return stdscr

    def _test_window_run(self, stdscr):
        curses.use_default_colors()
        curses.resizeterm(24, 80)
        curses.curs_set(False)

        stdscr.addstr(0, 0, "Score: 10923")
        nw = stdscr.derwin(1, 0)
        nw.border()
        x, y = 0, 0

        while 1:
            k = stdscr.getch()
            if k == ord('q'):
                break
            elif k == ord('h'):
                x -= 1
            elif k == ord('l'):
                x += 1
            elif k == ord('j'):
                y += 1
            elif k == ord('k'):
                y -= 1

            nw.clear()
            nw.border()
            stdscr.addstr(0, 20, "{:02} {:02}".format(x, y))
            nw.addch(y+1, x+1, '@')

            stdscr.noutrefresh()
            nw.noutrefresh()
            curses.doupdate()

    def _test_window_dispose_curses(self, stdscr):
        stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

if __name__ == "__main__":
    unittest.main()
