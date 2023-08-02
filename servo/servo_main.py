#pip install pyFirmata
#IDLE

from pyFirmata import Arduino, SERVO
import time 

board = Arduino('COM1') #change Port

servo1 = board.digital[9] #change pin
servo1.mode = SERVO

#set angle to 0
servo1.write(0)

time.sleep(2)
servo1.write(180)