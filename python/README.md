# Standalone Python Application

This directory contains the standalone application for reading ENS160
measurements on a PC through a USB-connected microcontroller. ROS 2 and a
Raspberry Pi are not required for this workflow.

The reader accepts the text protocol produced by the included firmware and
prints one JSON object per sensor sample. It can also append samples to CSV.

## 1. Prerequisites

- Python 3.10 or newer.
- A microcontroller connected to the PC through USB.
- The ENS160 connected to that microcontroller through I2C.
- Git and VS Code are optional but recommended.

The exact board, pins, voltage levels and Arduino libraries must be confirmed
before uploading firmware. See [Hardware and wiring](../docs/1_wiring.md).

## 2. Create a virtual environment

Run these commands from the repository root.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Ubuntu:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install the Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r python/requirements.txt
```

Arduino libraries are installed through the Arduino toolchain, not through
pip. These requirements do not install ROS 2.

## 4. Select the environment in VS Code

1. Install the **Python** extension from Microsoft if it is not installed.
2. Open the Command Palette with **Ctrl+Shift+P**.
3. Choose **Python: Select Interpreter**.
4. Select the interpreter from this repository's `.venv` directory.

If it is not listed, choose **Enter interpreter path** and browse to:

| System | Interpreter path relative to the repository root |
| --- | --- |
| Windows | `.venv/Scripts/python.exe` |
| Ubuntu | `.venv/bin/python` |

Open a new terminal and verify which Python it uses. If necessary, activate
the environment manually using the command for your system above.

## 5. Verify the setup

```bash
python -c "import sys; print(sys.executable)"
python -c "import serial; print(serial.__version__)"
```

The first command should print a path inside this repository's `.venv`.
The second should print the installed pyserial version.

You can list detected serial ports without running the sensor application:

```bash
python -m serial.tools.list_ports
```

The microcontroller must be connected for its port to appear. Typical names
include `COM3` on Windows and `/dev/ttyACM0` on Ubuntu. After installing the
project's `udev` rule, use the persistent `/dev/ens160` alias.

## 6. Run the application

First detect the available serial ports:

```bash
python python/read_air_quality.py --list-ports
```

Then pass the detected port to `python/read_air_quality.py`.

Windows:

```powershell
python python/read_air_quality.py --port COM3 --baud 9600
```

Ubuntu:

```bash
python python/read_air_quality.py --port /dev/ens160 --baud 9600
```

Use the baud rate configured in the firmware. Close the Arduino Serial
Monitor and any ROS serial reader before opening the same port in Python.

To save readings as CSV, add for example `--csv measurements/run01.csv`.

## 7. Resume work in a later session

You do not need to create the environment again. Open the repository,
activate the existing `.venv`, and run the application.

If `requirements.txt` changed after a Git update, install its dependencies
again:

```bash
python -m pip install -r python/requirements.txt
```

To leave the activated environment:

```bash
deactivate
```

## Git exclusions

Ensure the root `.gitignore` includes these entries, adding any that are
missing:

```gitignore
.venv/
__pycache__/
*.py[cod]
```

Commit `requirements.txt`, application code and documentation. Do not commit
the virtual environment. If `.venv` was already tracked, adding it to
`.gitignore` alone does not remove it from Git tracking.

## Related documentation

- [Hardware and wiring](../docs/1_wiring.md)
- [Project integration and Git synchronization](../docs/2_integration.md)
- [Persistent Linux device name](../docs/3_udev_rules.md)
- Firmware notes: `arduino/README.md`.

This `.venv` setup is for standalone Python. Follow the separate ROS 2 guide
for building and running the ROS package.
