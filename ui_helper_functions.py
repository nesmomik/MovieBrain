from subprocess import call
import os


def print_message(message):
    '''prints message in the middle of the ui'''
    clear_screen()

    print_title()

    print(f"\n\n\n\n  {message}\n\n\n")


def wait_for_enter():
    '''pause until press of enter key'''
    input("\n\n  Press the Enter key to continue!\n  ")


def clear_screen():
    '''empties the terminal in unix and windows'''
    call("clear" if os.name == "posix" else "cls")


def print_title():
    '''print the ascii art title'''
    print(r"""
  ___  ___           _     ______           _       
  |  \/  |          (_)    | ___ \         (_)      
  | .  . | _____   ___  ___| |_/ /_ __ __ _ _ _ __  
  | |\/| |/ _ \ \ / / |/ _ \ ___ \ '__/ _` | | '_ \ 
  | |  | | (_) \ V /| |  __/ |_/ / | | (_| | | | | |
  \_|  |_/\___/ \_/ |_|\___\____/|_|  \__,_|_|_| |_|                                                                                  
    """)


def print_brain():
    '''print the cute little brain'''
    print(r"""
                       _.--'"'.
                      (  ( (   )
                      (o)_    ) )
                          (o)_.'
                            )/
    """)


def print_intro():
    '''print intro screen'''
    clear_screen()

    print_title()

    print_brain()

    print("               Welcome to the MovieBrain!")


def print_menu():
    '''pring the main menu'''
    print_title()

    print(r"""
  Menu:

  1. List movies            6. Random movie
  2. Add movie              7. Search movie
  3. Delete movie           8. Movies sorted by rating
  4. Update movie           9. Show intro screen
  5. Show stats             0. Leave the MovieBrain
     
    """)
