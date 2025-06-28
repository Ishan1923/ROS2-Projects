import rclpy
from rclpy.node import Node

class my_node(Node):
	def __init__(self):
		super().__init__('my_first_node')
		self.create_timer(1.0, self.timer_callback)
	def timer_callback(self):
		self.get_logger().info("ROS2 says hello")

def main(args = None):
	rclpy.init(args = args)
	node = my_node()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__== '__main__':
	main()

