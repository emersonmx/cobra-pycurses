import curses
import unittest


class TestWindowLayout(unittest.TestCase):

    def test_window(self):
        error_code = 0
        try:
            curses.wrapper(self._test_window_run)
        except:
            error_code = 1

        self.assertEqual(error_code, 0)

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

            nw.erase()
            nw.border()
            stdscr.addstr(0, 20, "{:02} {:02}".format(x, y))
            nw.addch(y+1, x+1, '@')

            stdscr.noutrefresh()
            nw.noutrefresh()
            curses.doupdate()

if __name__ == "__main__":
    unittest.main()
