import serial
from time import sleep

# Config
rpi = '/dev/ttyACM0'
local = '/dev/tty.usbmodem1411'
ser = serial.Serial(local, 14400)
counter = 32 # Below 32 everything in ASCII is gibberish

def serialcom():
	while True:
			global counter
			counter +=1
			ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
			print ser.readline() # Read the newest output from the Arduino
			sleep(.1) # Delay for one tenth of a second
			if counter == 255:
				counter = 32

serialcom()



