# ROS 2 Integration

This directory contains two ROS 2 packages:

- `ens160_interfaces`: the `ENS160Reading` message definition.
- `ens160_air_quality_ros`: the USB serial reader and publisher node.

## Build

From the root of a ROS 2 workspace containing this repository:

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run

```bash
ros2 launch ens160_air_quality_ros air_quality.launch.py \
  port:=/dev/ens160 baud_rate:=9600
```

Replace the port with the actual device. The node publishes one
`ens160_interfaces/msg/ENS160Reading` message per sensor sample on
`/ens160/readings`.

Inspect the stream with:

```bash
ros2 topic echo /ens160/readings
```

Only one program can open the serial port at a time. Stop the standalone
Python reader and the Arduino Serial Monitor before starting this node.

See [the integration guide](../docs/2_integration.md) for workspace integration
and Git synchronization.
