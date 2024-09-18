import curses
import time

def boot_screen(stdscr):
    # Clean screen
    stdscr.clear()

    boot_time = 5
    height, width = stdscr.getmaxyx()
    message = "Booting up..."

    # Get the screen center
    y = height // 2
    x = (width - len(message)) // 2

    # Show the message
    stdscr.addstr(y, x, message)

    stdscr.refresh()
    time.sleep(boot_time)
    stdscr.clear()
    stdscr.refresh()

def main():
    curses.wrapper(boot_screen)

if __name__ == "__main__":
    main()
