# Hardware and Wiring

## Hardware

- Air quality sensor: ENS160 breakout board.
- Microcontroller: to be confirmed.
- Optional temperature and humidity sensor: to be confirmed.
- Host: PC connected to the microcontroller through USB.

## Connections

The ENS160 communicates with the microcontroller through I2C.
The microcontroller sends sensor readings to the PC through USB serial.

Exact pin connections and voltage levels must be documented
after identifying the breakout board and microcontroller.

## Firmware

The same firmware is used by the standalone Python application
and the ROS 2 node.

Only one application should access the serial port at a time.
