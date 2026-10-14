#!/usr/bin/env python3
"""ROS 2 node that publishes ENS160 serial measurements."""

import serial

import rclpy
from rclpy.node import Node

from ens160_interfaces.msg import ENS160Reading

from .protocol import parse_reading


class AirQualityNode(Node):
    def __init__(self) -> None:
        super().__init__("air_quality_node")
        self.declare_parameter("port", "/dev/ens160")
        self.declare_parameter("baud_rate", 9600)
        self.declare_parameter("timeout", 0.05)
        self.declare_parameter("poll_period", 0.02)

        port = self.get_parameter("port").value
        baud_rate = self.get_parameter("baud_rate").value
        timeout = self.get_parameter("timeout").value
        poll_period = self.get_parameter("poll_period").value

        self.publisher = self.create_publisher(ENS160Reading, "ens160/readings", 10)
        try:
            self.serial = serial.Serial(port, baud_rate, timeout=timeout)
        except serial.SerialException as error:
            self.get_logger().fatal(f"Cannot open {port}: {error}")
            raise

        self.timer = self.create_timer(poll_period, self.poll_serial)
        self.get_logger().info(f"Reading ENS160 data from {port} at {baud_rate} baud")

    def poll_serial(self) -> None:
        while self.serial.in_waiting:
            raw = self.serial.readline()
            line = raw.decode("utf-8", errors="replace").strip()
            reading = parse_reading(line)
            if reading is None:
                if line:
                    self.get_logger().debug(f"Device message: {line}")
                continue

            message = ENS160Reading()
            message.stamp = self.get_clock().now().to_msg()
            message.sensor_millis = reading.sensor_millis
            message.channel = reading.channel
            message.eco2_ppm = reading.eco2_ppm
            message.tvoc_ppb = reading.tvoc_ppb
            message.aqi = reading.aqi
            message.resistance_ohm = list(reading.resistance_ohm)
            self.publisher.publish(message)

    def destroy_node(self) -> bool:
        if hasattr(self, "serial") and self.serial.is_open:
            self.serial.close()
        return super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = AirQualityNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
