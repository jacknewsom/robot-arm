import warnings
import time
import serial
import serial.tools.list_ports

class ArduinoControl():
	def __init__(self):
		self.ser = None

	#Automatically connect to arduino
	def connect(self):
		arduino_ports = [
	    p.device
	    for p in serial.tools.list_ports.comports()
	    if 'Generic' in p.description 	#Change to REGEX (Generic|Arduino)
		]
		if not arduino_ports:
		    raise IOError("No Arduino found")
		if len(arduino_ports) > 1:
		    warnings.warn('Multiple Arduinos found - using the first')

		self.ser = serial.Serial(arduino_ports[0])


	#motor num = 1-4, motor_dir 1 or 0, motor_angle 000-360
	def move_motor(self, motor_num=0, motor_dir=0, motor_angle=0):
		motor_instructions = str(motor_num) + str(motor_dir) + str(motor_angle)
		print("Motor instructions: " + str(motor_instructions))
		print("Serial binary input: " + str(motor_instructions.encode()))
		self.ser.write(motor_instructions.encode())


if __name__ == "__main__":
	ac = ArduinoControl()
	ac.connect()
	ac.move_motor(1,1,1)

