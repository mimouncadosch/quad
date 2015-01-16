from flask import Flask, render_template
import serial
from time import sleep


app = Flask(__name__)


# Quadcopter variables
m0 = 0
m1 = 0
m2 = 0
m3 = 0
step = 1
yaw = 0
pitch = 0
roll = 0

# Config
rpi = '/dev/ttyACM0'
local = '/dev/tty.usbmodem1411'
ser = serial.Serial(local, 9600)
counter = 32 # Below 32 everything in ASCII is gibberish

# @app.route("/updating")
# def serialcom():
# 	global m0, m1, m2, m3
# 	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}

# 	while True:
# 		global counter
# 		counter +=1
# 		ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
# 		line = ser.readline() # Read the newest output from the Arduino
# 		ahrs = parse_line(line)
# 		sleep(.5) # Delay for one tenth of a second
# 		if counter == 255:
# 			counter = 32
# 		return ahrs

def parse_line(line):
	global yaw, pitch, roll
	global ahrs
	if line.find('Yaw') != -1:
		yaw = line

	elif line.find('Pitch') != -1:
		pitch = line

	elif line.find('Roll') != -1:
		roll = line
		
	ahrs = {"yaw":yaw, "pitch":pitch, "roll":roll}
	return ahrs
	
@app.route("/serialcom")
def serialcom():
	global counter

	while True:
		counter += 1
		ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
		line = ser.readline() # Read the newest output from the Arduino
		ahrs = parse_line(line)

		print 'ahrs', ahrs
		sleep(.5) # Delay for one tenth of a second
		if counter == 255:
			counter = 32

		return ahrs

@app.route("/")
def hello():
	global m0, m1, m2, m3, ahrs, counter
	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	
	return render_template('home.html', motorVals=motorVals)
	

@app.route("/throttle/<step>")
def throttle(step):
	global m0, m1, m2, m3
	step = int(step)
	if step == 1:
		print 'Throttle Up'
		ser.write('S')
	elif step == -1:
		print 'Throttle Down'
		ser.write('D')	
	m0 += step
	m1 += step
	m2 += step
	m3 += step

	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	motorVals = normalizeVals(motorVals)

	return render_template('home.html', motorVals=motorVals)
	
@app.route("/yaw/<step>")
def yaw(step):
	global m0, m1, m2, m3
	step = int(step)
	if step == 1:
		print 'Yaw Right'
		ser.write('F')
	elif step == -1:
		print 'Yaw Left'
		ser.write('A')
	m0 += step
	m2 += step

	m1 -= step
	m3 -= step

	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	motorVals = normalizeVals(motorVals)

	return render_template('home.html', motorVals=motorVals)


@app.route("/pitch/<step>")
def pitch(step):
	global m0, m1, m2, m3
	step = int(step)
	if step == 1:
		print 'Pitch Fwd'
		ser.write('J')
	elif step == -1:
		print 'Pitch Bkwd'
		ser.write('K')
	m0 -= step
	m1 -= step

	m2 += step
	m3 += step

	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	motorVals = normalizeVals(motorVals)

	return render_template('home.html', motorVals=motorVals)

@app.route("/roll/<step>")
def roll(step):
	global m0, m1, m2, m3
	step = int(step)
	if step == 1:
		print 'Roll Right'
		ser.write('L')
	elif step == -1:
		print 'Roll Left'
		ser.write('H')
	m0 += step
	m3 += step

	m1 -= step
	m2 -= step

	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	motorVals = normalizeVals(motorVals)

	return render_template('home.html', motorVals=motorVals)

# Normalize motor values, between 0 and 180
def normalizeVals(motorVals):
	for key in motorVals:
		print motorVals[key]
		if motorVals[key] < 0:
			motorVals[key] = 0
		elif motorVals[key] > 180:
			motorVals[key] = 180
	return motorVals

@app.route("/safetystop")
def safetystop():
	global m0, m1, m2, m3
	print "SAFETY STOP"
	ser.write('P')
	m0 = 0
	m1 = 0
	m2 = 0
	m3 = 0
	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	return render_template('home.html', motorVals=motorVals)

@app.route("/closeserial")
def closeserial():
	global m0, m1, m2, m3
	motorVals = {"m0":m0, "m1":m1, "m2":m2, "m3":m3}
	ser.close()
	print ser.readable
	return render_template('home.html', motorVals=motorVals)


	
if __name__ == "__main__":
	app.run(debug=True)

