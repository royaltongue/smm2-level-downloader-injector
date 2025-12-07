import requests
import numpy as np
import os

print("Please enter the level code for the level you would like to download in the format: ABCDEFGHI")
level_code = input()
print(f"The level code is {level_code}")

all_level_slots = [120,121,122,123,124,125,126,127,128,129,
                   130,131,132,133,134,135,136,137,138,139,
                   140,141,142,143,144,145,146,147,148,149,
                   150,151,152,153,154,155,156,157,158,159,
                   160,161,162,163,164,165,166,167,168,169,
                   170,171,172,173,174,175,176,177,178,179]
all_level_slots = np.array(all_level_slots)
#print(all_level_slots)

with open('history.txt', 'r') as history: # Import history file as properly formatted array
    level_history = [int(x) for x in history] 

print("You have previously saved levels to slots: " + str(level_history))
available_slots = np.setdiff1d(all_level_slots, level_history) # Take difference of all slots and previously used slots
print(f"Available slots are: " + str(available_slots))

print("What slot would you like to save this level in?")
level_slot = input()
print(f"The level will be saved in slot {level_slot}")
with open('history.txt', 'a') as history: # Add selected level slot to history file
    history.write("\n" + level_slot)
slot_filename = "course_data_" + level_slot + ".bcd" 

api_endpoint = "https://tgrcode.com/mm2/level_data/" # Public API for Mario Maker 2 level data hosted by TheGreatRambler
level_url = api_endpoint + level_code
file_destination = "./output/" + slot_filename
request = requests.get(level_url)
open(file_destination,'wb').write(request.content)

with open('smm2-save-directory.txt', 'r') as saveDirectory: # Read emulator save directory
    save_directory = saveDirectory.read()

moved_destination = save_directory + "/" + slot_filename
os.replace(file_destination, moved_destination)