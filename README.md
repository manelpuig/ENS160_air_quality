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

- [1. Hardware and wiring](docs/1_wiring.md)
- [2. Project integration and Git synchronization](docs/2_integration.md)
- [3. Persistent Linux device name](docs/3_udev_rules.md)

## Quick start

List serial ports and run the standalone reader:

```bash
python -m pip install -r python/requirements.txt
python python/read_air_quality.py --list-ports
python python/read_air_quality.py --port COM3 --baud 9600
```

On Linux, install the documented `udev` rule and use `/dev/ens160`, or use the
detected `/dev/ttyACM*` device until the persistent alias is configured.
See the directory-specific READMEs for firmware upload and ROS 2 commands.

## Status

The serial protocol, standalone reader, six-sensor Arduino firmware and ROS 2
publisher are implemented. Hardware validation is still required on the
physical controller and ENS160 array.
