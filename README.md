# ENS160 Air Quality

Air quality monitoring using an ENS160 sensor and a USB-connected
microcontroller.

## Execution Modes

- **Standalone Python:** read sensor data on a PC without ROS 2.
- **ROS 2:** publish sensor data in a robot workspace.

Both modes use the same microcontroller firmware.
A Raspberry Pi is not required for the standalone PC workflow.

## Repository Contents

| Directory | Contents |
| --- | --- |
| python | Standalone application, dependencies and Arduino firmware |
| ros2 | ROS 2 package |
| docs | Hardware wiring and project integration guides |

## Documentation

- [Hardware and wiring](docs/wiring.md)
- [Project integration and Git synchronization](docs/integration.md)

## Status

Initial repository structure. Firmware and application code
are under development.