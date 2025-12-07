from subprocess import call
import os


def print_message(message):
    """prints message in the middle of the ui"""
    clear_screen()

    print_title()

    print(f"\n\n\n\n  {message}\n\n\n")


def wait_for_enter():
    """pause until press of enter key"""
    input("\n\n  Press the Enter key to continue!\n  ")


def clear_screen():
    """empties the terminal in unix and windows"""
    call("clear" if os.name == "posix" else "cls")


def print_title():
    """print the ascii art title"""
    print(r"""
  ___  ___           _     ______           _
  |  \/  |          (_)    | ___ \         (_)
  | .  . | _____   ___  ___| |_/ /_ __ __ _ _ _ __
  | |\/| |/ _ \ \ / / |/ _ \ ___ \ '__/ _` | | '_ \
  | |  | | (_) \ V /| |  __/ |_/ / | | (_| | | | | |
  \_|  |_/\___/ \_/ |_|\___\____/|_|  \__,_|_|_| |_|
      """)


def print_goodbye():
    """print the ascii art goodbye"""
    print(r"""
     _____                 _______            _
    |  __ \               | | ___ \          | |
    | |  \/ ___   ___   __| | |_/ /_   _  ___| |
    | | __ / _ \ / _ \ / _` | ___ \ | | |/ _ \ |
    | |_\ \ (_) | (_) | (_| | |_/ / |_| |  __/_|
     \____/\___/ \___/ \__,_\____/ \__, |\___(_)
                                    __/ |
                                   |___/
      """)


def print_brain():
    """print the cute little brain"""
    print(r"""
                       _.--'"'.
                      (  ( (   )
                      (o)_    ) )
                          (o)_.'
                            )/
    """)


def print_intro():
    """print intro screen"""
    clear_screen()

    print_title()

    print_brain()

    print("               Welcome to the MovieBrain!")


def print_exit():
    """print exit screen"""
    clear_screen()

    print_goodbye()

    print_brain()

    print("           See you again in the MovieBrain!\n\n")


def print_user_menu():
    """print the user menu"""
    print(r"""
  Please choose:

  1. Log In User
  2. Add User
  3. Delete User
""")

def print_menu():
    """pring the main menu"""
    print_title()

    print(r"""
  Menu:

  1. List movies            6. Random movie
  2. Add movie              7. Search movie
  3. Delete movie           8. Sort movies
  4. Add/Update note        9. Filter movies
  5. Show stats             0. Leave the MovieBrain

    """)


def print_sort_menu():
    """print the sort menu options"""

    print(r"""
  How do you wish to sort the movies:

  1. By rating ascending
  2. By rating descending
  3. By year ascending
  4. By year descending


""")


def print_filter_menu():
    """print the sort menu options"""

    print(r"""
  How do you wish to filter the movies:

  1. By rating ascending
  2. By rating descending
  3. By year ascending
  4. By year descending


""")


def print_sub_menu(sub_type):
    """
    Prints the sort or filter sub menu according to the sub_type and returns
    the sort/filter options according to user choice
    """
    if sub_type == "sort":
        print_sort_menu()
    elif sub_type == "filter":
        print_filter_menu()
    else:
        print_message("Error: Wrong option passed to print_sub_menu.")
        return

    choice = input("  Enter choice! ")
    clear_screen()

    if choice == "1":
        info_type = "rating"
        bool_direction = False
    elif choice == "2":
        info_type = "rating"
        bool_direction = True
    elif choice == "3":
        info_type = "year"
        bool_direction = False
    elif choice == "4":
        info_type = "year"
        bool_direction = True
    else:
        print_message("Sorry, invalid choice!")
        return

    return choice, info_type, bool_direction
