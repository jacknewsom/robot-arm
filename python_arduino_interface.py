import warnings
import time
import serial
import serial.tools.list_ports

#Automatically connect to arduino
def auto_arduino_connect():
	arduino_ports = [
	    p.device
	    for p in serial.tools.list_ports.comports()
	    if 'Arduino' in p.description
	]
	if not arduino_ports:
	    raise IOError("No Arduino found")
	if len(arduino_ports) > 1:
	    warnings.warn('Multiple Arduinos found - using the first')

	ser = serial.Serial(arduino_ports[0])


#motor num = 1-4, motor_dir 1 or 0, motor_angle 000-360
def move_motor(motor_num=0, motor_dir=0, motor_angle=0):
	motor_instructions = motor_num + motor_dir + motor_angle
	ser.write(motor_instructions.encode())


if __name__ == "__main__":
	auto_arduino_connect() 
