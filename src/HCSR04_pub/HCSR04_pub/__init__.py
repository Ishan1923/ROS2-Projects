import rclpy
from rclpy.node import Node as node
import RPi.GPIO as gpio
import time
from std_msgs.msg import String

class HCSR04(node):
	def __init__(self):
		super().__init__("hcsr04_node")

		self.publisher_ = self.create_publisher(String, 'topic', 10) # msg type, topic name, queue size
		timer_period = 1 #sec
		self.timer = self.create_timer(timer_period, self.timer_callback)


		#self.distance = 0
		#setting the pin map accr to gpio pin numbers
		gpio.setmode(gpio.BCM)

		self.trig_pin = 17
		self.echo_pin = 27
		gpio.setup(self.trig_pin, gpio.OUT)
		gpio.setup(self.echo_pin, gpio.IN)
		gpio.output(self.trig_pin, 0)
		print("initializing sensor.. | trig_pin = GPIO PIN 17 ; echo_pin = GPIO PIN 27")

		self.pulse_start = 0
		self.pulse_end = 0
		self.distance = 0

		time.sleep(2)


	def measure(self):

		self.pulse_start = 0;
		self.pulse_end = 0;

		#sending pulse for 10 us
		gpio.output(self.trig_pin, 1);
		time.sleep(0.000001)
		gpio.output(self.trig_pin, 0);

		#geting the timestamps for the recieved pulses via echo_pin ==>
		#getting the starting of pulse time stamp
		#wait for echo pin to get high with timeout
		timeout = time.time() + 0.1
		while gpio.input(self.echo_pin) == 0 and time.time() < timeout:
			#time.time() will keep updating the pulse_start timestamp until the input from echo_pin becomes 1
			self.pulse_start = time.time()
		#getting the ending time stamp for the reciving pulse
		#wait for echo pin to get low with timeout
		timeout = time.time() + 0.1
		while gpio.input(self.echo_pin) == 1 and time.time() < timeout:
			#time.time() will keep updating the pulse_end timestamp val as in above
			self.pulse_end = time.time()

		if self.pulse_start != 0 and self.pulse_end != 0 and self.pulse_end > self.pulse_start:
			duration = self.pulse_end - self.pulse_start
			distance = duration * 17150
			self.distance = round(distance, 3)
			print(f'Distance : {self.distance}')
		else:
			print("sensor-timeout; no valid reading")
			self.distance = -1

	def timer_callback(self):
		msg = String()
		self.measure()
		msg.data = 'distance: %d' % self.distance
		self.publisher_.publish(msg)
		self.get_logger().info('Publishing: "%s"' % msg.data)

	def __del__(self):
		gpio.cleanup()

def main(args = None):
	rclpy.init(args = args)
	node = HCSR04()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
