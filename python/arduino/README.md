# Sensor Firmware

[`ens160_serial/ens160_serial.ino`](ens160_serial/ens160_serial.ino) reads six
ENS160 sensors through a TCA9548A I2C multiplexer and streams their values over
USB serial. It is shared by the standalone Python application and the ROS 2
node.

## Configuration

The configuration recovered from the reference `ENS160_rUBot` project is:

| Item | Value |
| --- | --- |
| ENS160 I2C address | `0x52` |
| TCA9548A I2C address | `0x70` |
| Multiplexer channels | `0` to `5` |
| Sensor enable pin | `A6` |
| Serial rate | `9600` baud |
| Sampling interval | `1000 ms` |

Install the **ScioSense ENS16x** Arduino library before compiling. The exact
board selection and the electrical suitability of pin `A6` must be checked
against the physical controller before uploading.

## Serial protocol

The firmware writes one ASCII line for each available sensor:

```text
12345,CH2,eCO2=487,TVOC=19,AQI=1,R0=101,R1=202,R2=303,R3=404
```

The fields are sensor uptime in milliseconds, multiplexer channel, eCO2 in
ppm, TVOC in ppb, UBA AQI and the four raw resistance values. Startup and error
messages do not follow this format; both readers ignore those lines.
