# Hardware and Wiring

## Hardware

- Air quality sensors: six ENS160 breakout boards at I2C address `0x52`.
- I2C multiplexer: TCA9548A at address `0x70`, using channels 0 to 5.
- Microcontroller: Arduino-compatible board; the exact model is not identified in the reference repository.
- Optional temperature and humidity sensor: to be confirmed.
- Host: PC connected to the microcontroller through USB.

## Connections

Each ENS160 communicates with the microcontroller through the TCA9548A I2C
multiplexer. The reference firmware enables the sensor system with pin `A6`.
The microcontroller sends sensor readings to the PC through USB serial.

The controller's SDA, SCL and voltage connections must be checked on the
physical board before wiring. Do not infer supply voltage from the bare ENS160
chip specification: breakout boards may include regulators or level shifting.

## Firmware

The same firmware is used by the standalone Python application
and the ROS 2 node.

Its default serial configuration is `9600` baud and one sample per second.

Only one application should access the serial port at a time.
