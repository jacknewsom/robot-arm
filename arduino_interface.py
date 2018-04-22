import serial
import time

port = '/dev/cu.usbmodem1411'
arduino = serial.Serial(port, 9600)

motorSteps = 0
while  motorSteps != "exit":
	motorSteps = input("Input motor steps ('exit' to quit): ")
	if motorSteps != "exit":
		arduino.write(motorSteps.encode())