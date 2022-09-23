

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from carver_interfaces.srv import Goaly


class AddTwoIntsClientNode(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        self.call_add_two_ints_server(2.0, -5.8, 0.0, 0.0, 0.0, 1.0)
        # self.call_add_two_ints_server(3, 1)
        # self.call_add_two_ints_server(5, 2)

    def call_add_two_ints_server(self, x, y, z, roll, pitch, yaw):
        client = self.create_client(Goaly, "/goal")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Add Two Ints...")

        request = Goaly.Request()
        request.x = x
        request.y = y
        request.z = z
        request.roll = roll
        request.pitch = pitch
        request.yaw = yaw

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_add_two_ints, x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw))

    def callback_call_add_two_ints(self, future, x, y, z, roll, pitch, yaw):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()