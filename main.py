import curses
import time

def init_screen(stdscr, boot_time, message):
    height, width = stdscr.getmaxyx()
    y = height // 2
    x = (width - len(message)) // 2
    stdscr.addstr(y, x, message)

    stdscr.refresh()
    time.sleep(boot_time)
    stdscr.clear()
    stdscr.refresh()

def boot_screen(stdscr):
    stdscr.clear()
    init_screen(stdscr, 5, "Booting up...")

def welcome_screen(stdscr):
    stdscr.clear()
    stdscr.border()
    init_screen(stdscr, 2, "Welcome to TermOS!")

def main_screen(stdscr):
    stdscr.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    stdscr.border()

    # Menu items
    menu_items = ["File", "View", "Tools", "Help"]
    version = "TermOS v0.2"

    # https://docs.python.org/3/library/curses.html#curses.window.attron
    # Add "attr" from "background" applied to the current window
    stdscr.attron(curses.color_pair(1))
    x = 2
    
    # Show menu items
    for item in menu_items:
        stdscr.addstr(1, x, item)
        # Space between items
        x += len(item) + 2

    # Version tag
    height, width = stdscr.getmaxyx()
    stdscr.addstr(1, (width - len(version) - 2), version)
    # https://docs.python.org/3/library/curses.html#curses.window.attroff
    # Remove "attr" from "background" applied to the current window
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        
        # Ctrl + Q (ASCII 17) to exit
        if key == 17:
            break
                
def main(stdscr):
    stdscr = curses.initscr()
    
    # https://docs.python.org/3/library/curses.html#curses.curs_set
    # Disable cursor
    curses.curs_set(0)


    # https://docs.python.org/3/library/curses.html#curses.has_colors
    # Checks if the terminal can display colors
    if curses.has_colors():
        curses.start_color()
    
    boot_screen(stdscr)
    welcome_screen(stdscr)
    main_screen(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
