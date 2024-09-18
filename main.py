import curses
import time

def boot_screen(stdscr, boot_time):
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    message = "Booting up..."

    y = height // 2
    x = (width - len(message)) // 2
    stdscr.addstr(y, x, message)

    stdscr.refresh()
    time.sleep(boot_time)
    stdscr.clear()
    stdscr.refresh()

def welcome_screen(stdscr):
    stdscr.border()

    height, width = stdscr.getmaxyx()
    message = "Welcome to TermOS!"

    y = height // 2
    x = (width - len(message)) // 2
    stdscr.addstr(y, x, message)
    
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    boot_time = 5

    boot_screen(stdscr, boot_time)
    welcome_screen(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
