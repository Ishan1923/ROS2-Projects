import rclpy
import RPi.GPIO as gpio
import math.pi
import rospy
import tf
from geometry_msgs.msg import Quaternion
from std_msgs.msg import float32

def make_quaternion(angle):
	q = tf.transformations.quaternion_from_euler(0,0,angle)
	return Quaternion(*q)

def callback(req):
	angle = sensor.value()*2*pi / 100.0
	q = make_quaternion(angle)

class Joystick(rclpy):
	def __init__(self):
		super().__init__("Joystick")
		self.x = 0
		self.y = 0
		gpio.setmode(gpio.BCM)
		gpio.setup(18, gpio.IN)
		gpio.setup(19, gpio.IN)
	def print_vals(self):
		print(gpio.input(18), gpio.input(19))


def main(args = None):
	pass

if __name__ == '__main__':
	main()
