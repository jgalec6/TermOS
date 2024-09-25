import curses
import time

# For testing purposes
# TODO: Change this to a SQLite file
VALID_USERNAME = "admin"
VALID_PASSWORD = "passwd"

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

def login_screen(stdscr):
    attempts = 0
    max_attempts = 3
    height, width = stdscr.getmaxyx()

    # Login screen border
    border_height = 10
    border_width = 40
    login_border_y = (height // 2) - (border_height // 2)
    login_border_x = (width // 2) - (border_width // 2)

    while attempts < max_attempts:
        stdscr.clear()
        stdscr.border()

        # Title
        stdscr.addstr(login_border_y, login_border_x + 1, "Welcome! Please login :)", curses.A_BOLD)

        # Draw the frame for input fields
        for y in range(border_height):
            stdscr.addch(login_border_y + y, login_border_x, curses.ACS_VLINE)
            stdscr.addch(login_border_y + y, login_border_x + border_width - 1, curses.ACS_VLINE)

        for x in range(border_width):
            stdscr.addch(login_border_y, login_border_x + x, curses.ACS_HLINE)
            stdscr.addch(login_border_y + border_height - 1, login_border_x + x, curses.ACS_HLINE)

        # TODO: Don't put a fixed X when `addstr` or `move`, but based on the length of the str

        # User input
        stdscr.addstr(login_border_y + 2, login_border_x + 2, "User:")
        curses.curs_set(1)
        stdscr.move(login_border_y + 2, login_border_x + 8)
        user_input = ""

        # TODO: Optimize that shitty `while` with a function
        while True:
            key = stdscr.getch()

            # Enter (ASCII 10)
            if key == 10:
                break
            # Backspace (ASCII 127)
            elif key == 127:
                if user_input:
                    user_input = user_input[:-1]
                    stdscr.addstr(login_border_y + 2, login_border_x + 8, " " * 20)
                    stdscr.addstr(login_border_y + 2, login_border_x + 8, user_input)
                    stdscr.move(login_border_y + 2, login_border_x + 8 + len(user_input))
            else:
                user_input += chr(key)
                stdscr.addstr(login_border_y + 2, login_border_x + 8, user_input)
                stdscr.move(login_border_y + 2, login_border_x + 8 + len(user_input))

        # Pass input
        stdscr.addstr(login_border_y + 4, login_border_x + 2, "Password:")
        pass_input = ""
        stdscr.move(login_border_y + 4, login_border_x + 12)

        # TODO: Optimize this shitty `while` with a function too
        while True:
            key = stdscr.getch()

            # Enter (ASCII 10)
            if key == 10:
                break
            # Backspace (ASCII 127)
            elif key == 127:
                if pass_input:
                    pass_input = pass_input[:-1]
                    stdscr.addstr(login_border_y + 4, login_border_x + 12, " " * 20)
                    stdscr.addstr(login_border_y + 4, login_border_x + 12, "*" * len(pass_input))
                    stdscr.move(login_border_y + 4, login_border_x + 12 + len(pass_input))
            else:
                pass_input += chr(key)
                stdscr.addstr(login_border_y + 4, login_border_x + 12, "*" * len(pass_input))
                stdscr.move(login_border_y + 4, login_border_x + 12 + len(pass_input))
            
        # Auth
        if user_input == VALID_USERNAME and pass_input == VALID_PASSWORD:
            stdscr.addstr(login_border_y + 6, login_border_x + 2, "Successful login!", curses.A_BOLD)
            curses.curs_set(0)
            stdscr.refresh()
            time.sleep(2)
            # Valid auth, proceed to desktop
            return True
        else:
            # Try again boyo!
            attempts += 1
            stdscr.addstr(login_border_y + 6, login_border_x + 2, f"Wrong data!. Remaining attempts: {max_attempts - attempts}", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)

    # If too many attempts, show exit message
    stdscr.addstr(login_border_y + 8, login_border_x + 2, "Too many failed attempts. Turning off...", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(2)
    # Invalid auth, proceed to exit
    return False
            

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

    if login_screen(stdscr):
        main_screen(stdscr)
    else:
        return

if __name__ == "__main__":
    curses.wrapper(main)
