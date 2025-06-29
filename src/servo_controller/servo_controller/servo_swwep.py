
import rclpy
from rclpy.node import Node
import RPi.GPIO as gpio
from std_msgs.msg import Float64
import threading
import time

class ServoControllerNode(Node):
	def __init__(self):
		super().__init__('servo_controller')
		self.gpio_pin = 4
		gpio.setmode(gpio.BCM)
		gpio.setup(self.gpio_pin, gpio.OUT)
		self.pwm = gpio.PWM(self.gpio_pin, 50)
		self.pwm.start(0)
		self.thread = threading.Thread(target=self.sweep_loop)
		self.thread.start()

	def set_angle(self, angle):
		duty = 2.5 + (angle / 180.0) * 10
		self.pwm.ChangeDutyCycle(duty)
		time.sleep(0.03)

	def sweep_loop(self):
		while rclpy.ok():
			for angle in range(0,181, 5):
				self.set_angle(angle)
			for angle in range(180, -1, -5):
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
