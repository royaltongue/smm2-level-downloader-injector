import requests
import numpy as np
import os

# Prompt for level code
print("Please enter the level code for the level you would like to download in the format: ABCDEFGHI")
level_code = input()
print(f"The level code is {level_code}")

all_level_slots = [0,1,2,3,4,5,6,7,8,9, # Slots 0-119 are "My Course" and 120-179 are "Downloaded Courses"
                   10,11,12,13,14,15,16,17,18,19,
                   20,21,22,23,24,25,26,27,28,29,
                   30,31,32,33,34,35,36,37,38,39,
                   40,41,42,43,44,45,46,47,48,49,
                   50,51,52,53,54,55,56,57,58,59,
                   60,61,62,63,64,65,66,67,68,69,
                   70,71,72,73,74,75,76,77,78,79,
                   80,81,82,83,84,85,86,87,88,89,
                   90,91,92,93,94,95,96,97,98,99,
                   100,101,102,103,104,105,106,107,108,109,
                   110,111,112,113,114,115,116,117,118,119,
                   120,121,122,123,124,125,126,127,128,129,
                   130,131,132,133,134,135,136,137,138,139,
                   140,141,142,143,144,145,146,147,148,149,
                   150,151,152,153,154,155,156,157,158,159,
                   160,161,162,163,164,165,166,167,168,169,
                   170,171,172,173,174,175,176,177,178,179]
all_level_slots = np.array(all_level_slots)
#print(all_level_slots)

with open('history.txt', 'r') as history: # Import history file as properly formatted array
    level_history = [int(x.strip('\n')) for x in history] 

print("\nYou have previously saved levels to slots: " + str(level_history))
available_slots = np.setdiff1d(all_level_slots, level_history) # Take difference of all slots and previously used slots
print(f"Available slots are: " + str(available_slots))

print("\nWhat slot would you like to save this level in? \nSlots 0-119 are \"My Courses\" and editable, slots 120-179 are \"Downloaded Courses\"") # Prompt for level slot
level_slot = input()
print(f"The level will be saved in slot {level_slot}")
with open('history.txt', 'a') as history: # Add selected level slot to history file
    history.write(level_slot +'\n')
# Level slot filename must be 3 digits, this will add the appropriate amount of leading zeroes
if len(level_slot) == 1:
    appended_level_slot = "00" + level_slot
elif len(level_slot) == 2:
    appended_level_slot = "0" + level_slot
elif len(level_slot) == 3:
    appended_level_slot = level_slot
slot_filename = "course_data_" + appended_level_slot + ".bcd" 

api_endpoint = "https://tgrcode.com/mm2/level_data/" # Public API for Mario Maker 2 level data hosted by TheGreatRambler
level_url = api_endpoint + level_code
file_destination = "./output/" + slot_filename
request = requests.get(level_url) # Get level data file
open(file_destination,'wb').write(request.content) # Save level data file

with open('smm2-save-directory.txt', 'r') as saveDirectory: # Read emulator save directory
    save_directory = saveDirectory.read()

moved_destination = save_directory + "/" + slot_filename
os.replace(file_destination, moved_destination) # Move file to emulator save directory