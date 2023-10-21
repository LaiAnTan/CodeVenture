import os

# CONSTANTS WHICH DEFINES WHAT FILE NAMES AND WHICH PATH EVERYTHING
# IS STORED

# DO NOT MODIFY WITH NO GOOD REASON!
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSET_FOLDER = 'asset'
ASSET_DIR = f'{ROOT_DIR}/{ASSET_FOLDER}'
ACTIVITY_FOLDER = 'storeroom'
ACTIVITY_DIR = f'{ROOT_DIR}/{ACTIVITY_FOLDER}'
DATA_FILE = 'data.dat'

DEFAULT_IDE_MESSAGE = \
"""This is the IDE window

You can write your code here, then click on input button to write some input for your code to run with

Use this like how you would use any normal Python Editor!"""

DEFAULT_INPUT_MESSAGE = \
"""This is the Input window

You would write the input for your code to run with, for codes which requires input from your keyboard.

Each input must be seperated by a Enter key, if your output states "Reached EOF", that means you do not have enough input!"""