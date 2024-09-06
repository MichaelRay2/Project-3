from random import randrange
import time

# 3rd party
from colorama import fore

# Bringing in modules needed to link file to google doc
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('MR - Project 3')
# setting score_sheet variable to the sheet where all results will be stored
score_sheet = SHEET.worksheet('results')

# Using Fore and sleep time to make a game title
def head():
    print(Fore.RED + "=========================================================================================")
    time.sleep(1)        
    print(Fore.BLUE + "  |==||    // \\   ====== ======  ||     ||===  ||===  ||  ||  ==||==  ||==||  ||===      ")
    print(Fore.BLUE + "  |__||   //===\\    ||     ||    ||     ||===  ||=||  ||==||    ||    ||==||  ||=||  ")
    print(Fore.BLUE + "  |--||  //     \\   ||     ||    ||===  ||===  ===||  ||  ||  ==||==  ||      ===||    ")
    print(Fore.BLUE + "  |==||                                       ")
    time.sleep(1)           
    print(Fore.RED + "==========================================================================================")

# Explaining rules of the game
def intro():
    print(Fore.WHITE + "Welcome to Battleships!")
    print("During this game you will play against the computer and you will be asked to distribute 6 different ships around your board.")
    print("Your board and the Computer's board will look like the following:")
    print("  0 1 2 3 4 5 6 7 8 9")
    print("0 - - - - - - - - - -")
    print("1 - - - - - - - - - -")
    print("2 - - - - - - - - - -")
    print("3 - - - - - - - - - -")
    print("4 - - - - - - - - - -")
    print("5 - - - - - - - - - -")
    print("6 - o o o o o - - - -")
    print("7 - - - - - - - - - -")
    print("8 - - - - - - - - - -")
    print("9 - - - - - - - - - -")
    print("You must enter numbers such that the cells occupied by a single ship are adjacent to each other.")
    print("For the result shown in the grid above you would enter 61|62|63|64|65")
    print("Note: Your ships cannot be diagonal")