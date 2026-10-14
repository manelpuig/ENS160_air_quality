# Persistent Linux Device Name

Linux may assign a different `/dev/ttyACM*` name after reconnecting the board
or changing the USB connection order. A `udev` rule can create the stable
alias `/dev/ens160` for the Arduino used by the ENS160 array.

The rule must identify the physical device, not a guessed port number. Use its
USB vendor ID, product ID and unique serial number so that another Arduino is
not accidentally assigned the sensor alias.

## 1. Identify the device

Connect the board with its normal ENS160 firmware running and find its current
port:

```bash
python3 -m serial.tools.list_ports -v
```

Assuming it currently appears as `/dev/ttyACM1`, inspect its properties:

```bash
udevadm info --query=property --name=/dev/ttyACM1
udevadm info --attribute-walk --name=/dev/ttyACM1
```

Record these values from the physical board:

```text
ID_VENDOR_ID
ID_MODEL_ID
ID_SERIAL_SHORT
```

Do not copy identifiers from another Arduino Nano 33 IoT. The serial number is
what distinguishes the ENS160 controller from the robot motor controller.

## 2. Create the rule

Copy [`udev/99-ens160.rules.example`](../udev/99-ens160.rules.example) to a
temporary file named `99-ens160.rules`. Replace all three placeholder values:

```udev
SUBSYSTEM=="tty", ACTION=="add", ATTRS{idVendor}=="VENDOR_ID", ATTRS{idProduct}=="PRODUCT_ID", ATTRS{serial}=="SERIAL_NUMBER", SYMLINK+="ens160", GROUP="dialout", MODE="0660"
```

Install the completed rule:

```bash
sudo cp 99-ens160.rules /etc/udev/rules.d/99-ens160.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Unplug and reconnect the board, then verify the alias:

```bash
ls -l /dev/ens160
udevadm info --query=property --name=/dev/ens160
```

The symbolic link should resolve to the current `/dev/ttyACM*` device.

## 3. Serial-port permissions

Add the user to the serial-device group if necessary:

```bash
sudo usermod -a -G dialout "$USER"
```

Log out and back in before testing the new group membership. Avoid using
world-writable permissions such as `MODE="0666"`.

## 4. Run with the persistent name

Standalone Python:

```bash
python python/read_air_quality.py --port /dev/ens160 --baud 9600
```

ROS 2:

```bash
ros2 launch ens160_air_quality_ros air_quality.launch.py \
  port:=/dev/ens160 baud_rate:=9600
```

The default ROS 2 configuration uses `/dev/ens160`. Override `port` when the
rule has not yet been installed.
