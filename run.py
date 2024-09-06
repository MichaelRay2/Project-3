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


def check_ok(boat,taken):
    #Sort boats to make ascending list
    boat.sort()
    #For loop to account for reduction in spaces of boat left ifa a space has been taken
    for i in range(len(boat)):
        num = boat[i]
        if num in taken:
            boat = [-1]
            break
        elif num < 0 or num > 99:
            boat = [-1]
            break
        elif != 0:
            if boat[i] != boat[i-1]+1 and boat[i] != boat[i-1]+10:
                boat = [-1]
                break
        
        return boat
    
def get_ship(long,taken):
    #setting initial status of true for loop
    ok = True
    while ok:
        ship = []
        #ask user to enter numbers
        print("Enter your ship of length",long)
        for i in range(long):
            boat_num = input("Enter a number")
            #adding number user picked to ship list
            ship.append(int(boat_num))
            #checking that ship has been placed acceptably
            ship = check_ok(ship,taken)
            #-1 is the key for a failed placed ship. Re-assign taken to include new ship.
            if ship[0] != -1:
                taken = taken + ship
                break
                else:
                    print("error - please try again")

            return ship,taken

def create_ships(taken,boats):
    #assinging ships to empty list so we can append 
    ships = []

    for boat in boats:
        #running rhrough get_ship function and passing through boat and taken so we can assign the ship locations
        ship,taken = get_ship(boat,taken)
        ships.append(ship)

    return ships,taken

def check_boat(b,start,dirn,taken):
    #check that all numbers align
    boat = []
    if dirn == 1:
        for i in range(b):
            boat.append(start - i*10)
    elif dirn == 2:
        for i in range(b):
            boat.append(start + i)
    elif dirn == 3:
        for i in range(b):
            boat.append(start + i*10)
    elif dirn == 4:
        for i in range(b):
            boat.append(start - i)
    boat = check_ok(boat,taken)           
    return boat  

#Function to randomly generate boat positions for computer.
def create_boats(taken,boats):
    for b in boats:
        boat = [-1]
        while boat[0] == -1:
            #Assigning first position randomly
            boat_start = randrange(99)
            #Assigning direction randomly
            boat_direction = randrange(1,4)
            boat = check_boat(b,boat_start,boat_direction,taken)
        ships.append(boat)
        #important that taken is re-assigned so that no boats overlap
        taken = taken + boat

#function to show computer's board
def show_board_c(taken):
    print("            battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in taken:
                ch = " o "   
            row = row + ch
            place = place + 1
            
        print(x," ",row)

#generates computer's shot, with tactics
def get_shot_comp(guesses,tactics):
    # re-assigning var from "TRUE" to n
    ok = "n"
    while ok == "n":
        try:
            #Checks if tactics are applicable
            if len(tactics) > 0:
                shot = tactics[0]
            else:
                #Random shot if no tactics are applicable
                shot = randrange(99)
            if shot not in guesses:
                #Ensures shot has not already been done
                ok = "y"
                guesses.append(shot)
                break
        except:
            print("incorrect entry - please enter again")
            
    return shot,guesses

def show_board(hit,miss,comp):
    print("            battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in miss:
                ch = " x " 
            elif place in hit:
                ch = " o "
            elif place in comp:
                ch = " O "   
            row = row + ch
            place = place + 1
            
        print(x," ",row)

def check_shot(shot,ships,hit,miss,comp):
    missed = 0
    for i in range(len(ships)):      
        if shot in ships[i]:
            ships[i].remove(shot)
            if len(ships[i]) > 0:
                hit.append(shot)
                missed = 1
            else:
                comp.append(shot)
                missed = 2                              
    if missed == 0:
        miss.append(shot)
                
    return ships,hit,miss,comp,missed

#determining where next shot should be based on whether the previous shot was a hit
def calc_tactics(shot,tactics,guesses,hit):
    temp = []
    if len(tactics) < 1:
        temp = [shot-1,shot+1,shot-10,shot+10]
    else:
        if shot-1 in hit:
            temp = [shot+1]
            for num in [2,3,4,5,6,7,8]:
                if shot-num not in hit:
                    temp.append(shot-num) 
                    break 
        elif shot+1 in hit:
            temp = [shot-1]
            for num in [2,3,4,5,6,7,8]:
                if shot+num not in hit:
                    temp.append(shot+num) 
                    break
        if shot-10 in hit:
            temp = [shot+10]
            for num in [20,30,40,50,60,70,80]:
                if shot-num not in hit:
                    temp.append(shot-num) 
                    break 
        elif shot+10 in hit:
            temp = [shot-10]
            for num in [20,30,40,50,60,70,80]:
                if shot+num not in hit:
                    temp.append(shot+num) 
                    break

def get_shot(guesses):

def check_if_empty_2(list_of_lists):

#Maths Question to potentially multiply user's score
def maths_question():
    global score_mult 
    print("Now for the chance to multiply your score.")
    #Generating 2 random numbers
    num_1 = random.randint(4,12)
    num_2 = random.randint(4,12)
    print("What is " + (str(num_1)) + " x "+ (str(num_2) + " ?"))
    response = input()
    #Check to see if response is numeric
    while not response.isnumeric():
        print("Enter a number")
        response = input()
    response_int = int(response)
    answer = num_1*num_2

    #If statement to determine whether user's answer is correct and score should be multiplied by 2x.
    if answer == response_int:
        print("correct, your score is doubled")
        score_mult = 2
    else:
        print("Incorrect, your score stays the same")
        score_mult = 1

    #Printing the users final score
    final_score = score_mult*score
    print(final_score)

#Getting a name to store alongside user's score
def get_user_data():
    global username
    username = input("Enter a username")

#This function will update the scoresheet and pull the highest score in the column along with the corresponding username
def update_score_sheet():
    values = score_sheet.get_all_values
    #Defining last row of sheet
    last_row = len(values) + 1
    #New data to be added
    new_data = [username,score]
    #Inserting new row for new data
    score_sheet.insert_row(new_data, last_row)
    #Pulling highest number from 2nd column
    column_data = score_sheet.col_values(2)
    highest_number = max(column_data)
    #Pulling corresponding username on same row
    numeric_data = [float(value) for value in column_data if value]
    max_index = numeric_data.index(max(numeric_data)) + 1
    best_user = score_sheet.cell(max_index, 1).value
    #Prining the current high score and the username
    print("The player with that has the best score is " + best_user)
    print("Their highest score is: " + str(highest_number))