# Super Mario Maker 2 Level Downloader/Injector

# Attribution
Massive thanks to:

[TheGreatRambler](https://github.com/TheGreatRambler) - For making the [MariOver API](https://github.com/TheGreatRambler/MariOver) and making any of this possible 

[DarkFlare](https://www.youtube.com/@DarkFlare) - For creating a cheat to mostly remove background music from Mario Maker 2 in the description of [this video](https://www.youtube.com/watch?v=vQd758VzOug)

# Description
Leveraging the MariOver API, this **very rudimentary** tool will download Mario Maker 2 levels from the official Nintendo servers, rename them to a slot within Coursebot, and "inject" the level into a Mario Maker 2 save.

Through this, it becomes possible to inject levels into your "My Courses" section of Coursebot, thus granting you full editor access.

# Assumptions
Mario Maker 2 will refuse to acknowledge replaced level data files if the save file does not already have a level in that slot. For convenience, I've included my save file that has all 120 "My Courses" and 60 "Downloaded Courses" slots filled. This means you can freely use this tool on any available slot.

You are free to not use this included save file, but keep in mind that level slots will remain empty until you first save a level within the game, **then** replace the level file.

# Known Bugs
## IMPORTANT
This tool only replaces the **level data** and not the **level metadata**. As such, you will notice the following:
* Level thumbnails will not be the correct one from your replaced level
* Level statistics will not be the correct ones from your replaced level
* The maker will not be the correct one from your replaced level
* After loading into a level, the level card will be entirely incorrect

Some of these could be fixed by downloading further data from the MariOver API, but no promises I will get to that

# How To Use
0) **MAKE SURE YOUR EMULATOR IS CLOSED BEFORE INJECTING FILES**
1) Download and extract or clone this repository
2) Open `smm2-save-directory.txt` and set your where you would like these levels to be saved to

    a) If using an emulator such as Ryujinx, right click on Mario Maker 2 and select "Open User Save Directory". Copy this directory and make sure it is saved using forward-slash / and not back-slash \

    b) If using a homebrewed Switch, you can use the directory structure that I've shown in my Pre-loaded Save. You will need to then inject this save using Checkpoint
3) Open the directory in a terminal
4) `python -m venv venv` to set up the venv
5) If on Windows: `venv/Scripts/activate` to activate the env
6) `pip install -r requirements.txt`
7) `python smm2-level-downloader-injector.py`
8) Enter the level ID of the level you want to download in the format `ABCDEFGHI`, not case-sensitive
9) Select the level slot to inject this level

    a) Slots 0-119 are "My Courses" and have editor capabilities

    b) Slots 120-179 are "Downloaded Courses" and do not have editor capabilities
10) Open your emulator, or inject the save using Checkpoint, and the level should now be in Coursebot

# Bonus
If you are playing in Ryujinx, you can remove the background music from Mario Maker 2 while still keeping all of the shell bops and other sound effects

1) In Ryujinx, right click Mario Maker 2 and select "Open Mods Directory"
2) Copy entire "cheats" folder to that directory
3) Back in Ryujinx, right click Mario Maker 2 again and select "Manage Cheats"
4) Ensure the cheat is enabled, and save