
import rclpy
from rclpy.node import Node
import RPi.GPIO as gpio
from std_msgs.msg import Float64
import threading
import time

class ServoControllerNode(Node):
	def __init__(self):
		super().__init__('servo_controller')
		self.gpio_pin = 4 #setting the gpio pin
		gpio.setmode(gpio.BCM) #To set the pin numbering as same as the gpio pin numbering on the board (Broadcom soc channel)
		gpio.setup(self.gpio_pin, gpio.OUT)	#pinmode; whether the specified pin will be used for input or output operations
		self.pwm = gpio.PWM(self.gpio_pin, 50)	#setting the duty cycle for the signal on the pin; here it is 50%
		self.pwm.start(0) #to initially start at del theta = 0deg
		self.thread = threading.Thread(target=self.sweep_loop) #making a parallel thread to do the task asynchronously
		self.thread.start() #startign the parallerl thread
		print("initialized ServoControllerNode use gpio pin 4 for servo control")
		print("setting the servo at 0 degrees")
		self.set_angle(0);

	def set_angle(self, angle):
		duty = 2.5 + (angle / 180.0) * 10
		self.pwm.ChangeDutyCycle(duty)
		time.sleep(0.03)

	def sweep_loop(self):
		while rclpy.ok():
			for angle in range(0,120, 1):
				self.set_angle(angle)
			for angle in range(120, 0, -1):
				self.set_angle(angle)

	def angle_callback(self, msg):
		angle = msg.data
		duty = 2.5 + (angle / 180.0)*10
		self.get_logger().info(f"settings angle: {angle} deg, PWM: {duty: .2f}%")
		self.pwm.ChangeDutyCycle(duty)

	def destroy_node(self):
		self.pwm.stop()
		gpio.cleanup()
		super().destroy_node()

def main(args = None):
	print("Starting Servo Node")
	rclpy.init(args = args)
	node = ServoControllerNode()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		node.get_logger().info('shutting dowm...')
	finally:
		node.destroy_node()
		rclpy.shutdown()
