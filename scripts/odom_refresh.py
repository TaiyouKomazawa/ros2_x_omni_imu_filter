#! /usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty

class OdomRefreshClient(Node):

    def __init__(self):
        super().__init__('odom_refresh_node')
        self.odom_cli = self.create_client(Empty, 'x_omni/odom_reset')
        self.imu_cli = self.create_client(Empty, 'x_omni/imu_calibration')
        while not self.odom_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('odom service not available, waiting again...')
        self.odom_req = Empty.Request()
        while not self.imu_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('imu service not available, waiting again...')
        self.imu_req = Empty.Request()

    def send_request(self):
        self.odom_future = self.odom_cli.call_async(self.odom_req)
        self.imu_future = self.imu_cli.call_async(self.imu_req)

def main():
    rclpy.init()

    node = OdomRefreshClient()
    node.send_request()

    while rclpy.ok():
        rclpy.spin_once(node)
        if node.odom_future.done() and node.imu_future.done():
            try:
                node.get_logger().info('Imu and Odometry reset service were done.')
                node.odom_future.result()
                node.imu_future.result()
            except Exception as e:
                node.get_logger().info(
                    'Service call failed %r' % (e,))
            break


    node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
