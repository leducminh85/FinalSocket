import keyboard
import time

for i in range(150):
    keyboard.block_key(i)

time.sleep(5)

for i in range(150):
    keyboard.unblock_key(i)
    