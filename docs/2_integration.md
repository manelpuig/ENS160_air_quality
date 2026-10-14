# ENS160 Air Quality: Project Integration and Git Synchronization

## Purpose and scope

This guide proposes one repository, `ENS160_air_quality`, supporting two workflows:

- Standalone Python on a PC, without ROS 2 or a Raspberry Pi.
- ROS 2 integration in a robot workspace, alongside `my_rUBot_mecanum`.

The repository includes a standalone serial reader, Arduino firmware and ROS 2 packages. The hardware-specific configuration is based on the reference `ENS160_rUBot` project and must still be validated on the physical controller. Git commands apply once the repositories exist and access is configured.

## Sensor and software names

ENS160 is the model of a ScioSense digital metal-oxide multi-gas sensor. It provides air-quality indicators including AQI, TVOC and equivalent CO₂ (eCO₂). eCO₂ is an estimate, not a direct CO₂ measurement.

If the breakout board also contains a temperature/humidity sensor, that is an additional device; its model and driver must be identified separately.

Use these distinct names:

| Component | Proposed name |
| --- | --- |
| Git repository | `ENS160_air_quality` |
| ROS 2 package | `ens160_air_quality_ros` |
| Standalone Python application | `python/read_air_quality.py` |

A repository can contain firmware, Python programs, documentation and ROS packages. Its name does not have to match its ROS package name.

## Proposed repository layout

Keep two main implementation directories, `python/` and `ros2/`, plus shared documentation at the repository root.

| Path | Purpose |
| --- | --- |
| `README.md` | Overview and links to setup guides |
| `docs/1_wiring.md` | Exact hardware, pin connections, voltage levels and USB connection |
| `docs/2_integration.md` | This guide: project integration and synchronization |
| `docs/3_udev_rules.md` | Persistent Linux device name and serial permissions |
| `python/COLCON_IGNORE` | Empty marker preventing colcon from scanning this directory |
| `python/requirements.txt` | Dependencies for the standalone Python application |
| `python/ens160_serial.py` | Parser and typed representation of one sensor record |
| `python/read_air_quality.py` | Standalone serial reader |
| `python/arduino/ens160_serial/ens160_serial.ino` | Firmware reading the sensor and transmitting data over USB serial |
| `ros2/ens160_interfaces/msg/ENS160Reading.msg` | Typed ROS 2 sensor message |
| `ros2/ens160_air_quality_ros/package.xml` | ROS package metadata and dependency declarations |
| `ros2/ens160_air_quality_ros/setup.py` | ROS Python package installation and executable entry points |
| `ros2/ens160_air_quality_ros/setup.cfg` | ROS executable installation settings |
| `ros2/ens160_air_quality_ros/resource/ens160_air_quality_ros` | Package marker for the ament resource index |
| `ros2/ens160_air_quality_ros/ens160_air_quality_ros/__init__.py` | Python package marker |
| `ros2/ens160_air_quality_ros/ens160_air_quality_ros/air_quality_node.py` | ROS serial reader and publisher |
| `ros2/ens160_air_quality_ros/launch/` | Sensor launch files |
| `ros2/ens160_air_quality_ros/config/` | Serial port, baud rate and publication settings |
| `.gitignore` | Excludes environments, caches and generated files |

Placing `requirements.txt` inside `python/` is appropriate. Placing Arduino firmware there also fits this two-directory organization, but the firmware is shared by both execution modes: upload it once, then use either the standalone reader or the ROS node.

Do not place `COLCON_IGNORE` at the repository root, because that would hide the ROS package too.

For a minimal serial reader, `python/requirements.txt` can start with:

```text
pyserial
```

Add plotting or analysis dependencies only when required. Arduino libraries are installed through the Arduino toolchain, not through pip. ROS dependencies belong in `package.xml`; installing the standalone requirements does not install ROS 2.

## Hardware architecture

The proposed PC workflow uses an Arduino-compatible board as an I²C-to-USB serial bridge:

1. The ENS160 breakout connects to the microcontroller over I²C.
2. Firmware reads the sensor and sends structured records over USB serial.
3. The PC runs either the Python application or the ROS node.

A Raspberry Pi is optional. An ordinary PC needs an interface such as this microcontroller or a supported USB-to-I²C adapter; a USB cable alone does not connect a bare ENS160 to the PC.

The firmware should provide the same documented serial format for both readers, including units and sensor validity status. Both readers must use the configured firmware baud rate. Only one reader should open the serial port at a time.

Confirm the exact microcontroller and breakout before specifying pin numbers or supply voltages. Bare-chip limits and breakout-board input limits may differ. Record verified connections in `docs/1_wiring.md`.

## Standalone Python on a PC

Clone the repository into a normal project directory:

```bash
git clone https://github.com/manelpuig/ENS160_air_quality.git
cd ENS160_air_quality
```

Upload the firmware using the appropriate Arduino board configuration and libraries, then create a Python environment.

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r python/requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r python/requirements.txt
```

The reader accepts `--port` and `--baud` arguments. With the included firmware configuration:

```bash
python python/read_air_quality.py --port /dev/ens160 --baud 9600
```

On Windows, replace the device path with the actual COM port, such as `COM3`. Port names and baud rate are examples, not confirmed hardware settings.

## Integration into a ROS 2 Humble workspace

These commands assume Ubuntu, ROS 2 Humble and colcon are installed. Create a workspace containing two independent clones:

```bash
mkdir -p ~/air_quality_robot_ws/src
cd ~/air_quality_robot_ws/src
git clone https://github.com/manelpuig/my_rUBot_mecanum.git
git clone https://github.com/manelpuig/ENS160_air_quality.git
```

If the robot repository is already present, clone only the sensor repository alongside it.

Each cloned repository retains its own `.git` directory. The sensor ROS package is nested under `ENS160_air_quality/ros2/`; colcon discovers nested packages recursively, while `python/COLCON_IGNORE` excludes the standalone directory.

Install declared dependencies and build:

```bash
cd ~/air_quality_robot_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon list
colcon build --symlink-install
```

Check that `colcon list` includes `ens160_air_quality_ros`. Dependency installation requires rosdep to have been initialized and updated.

In a new terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/air_quality_robot_ws/install/setup.bash
```

The ROS packages provide:

- An executable named `air_quality_node`.
- A launch file named `air_quality.launch.py`.
- Launch arguments for `port` and `baud_rate`.
- A typed `ENS160Reading` message published on `/ens160/readings`.

Launch it with:

```bash
ros2 launch ens160_air_quality_ros air_quality.launch.py port:=/dev/ens160 baud_rate:=9600
```

Run the robot bringup in another terminal using that repository's documented launch command. A robot-project launch file can later include both bringups. It does not need to copy the sensor code.

On Linux, use a stable device identifier or a dedicated udev alias when multiple serial devices are connected. The sensor bridge and the robot motor-controller board must have distinct ports.

## Synchronizing changes with the original repositories

Cloning creates a local working copy linked to a remote named `origin`. Cloning inside `src/` does not change that relationship.

Changes are synchronized per repository, not per workspace. From the sensor clone:

```bash
cd ~/air_quality_robot_ws/src/ENS160_air_quality
git remote -v
git branch --show-current
git status
git diff
```

Before starting work, with a clean working tree:

```bash
git pull --ff-only
```

After editing the integration guide, review and save that specific file:

```bash
git add docs/2_integration.md
git diff --cached
git commit -m "Document project integration and Git synchronization"
git push
```

Stage other intended files explicitly when editing code or firmware. The first push of a new branch may require `git push -u origin BRANCH_NAME`, replacing `BRANCH_NAME` with the actual branch.

Repeat this workflow from `src/my_rUBot_mecanum` for changes belonging to the robot repository. A push from the sensor directory does not upload robot changes, and vice versa.

Direct pushes require write permission to the destination repository. If you use a fork, `origin` normally points to your fork; contribute back through a pull request to the original repository.

If `git pull --ff-only` reports diverging history, review the branches and reconcile them with a merge or rebase. Do not use force-push as a routine synchronization step.

## Working from more than one local clone

A standalone PC clone and a ROS workspace clone can both point to the same remote:

1. Edit, commit and push in the first clone.
2. In the second clone, check `git status`.
3. Commit or stash any pending changes before updating.
4. Run `git pull --ff-only`.

Local copies do not update automatically. Git transfers committed changes through the remote; it does not synchronize uncommitted edits.

## Managing the complete robot project

For this setup, keep `src/` as a collection of independent repositories. Do not initialize a parent Git repository merely to synchronize its child clones.

If a separate project repository is needed, it can track workspace instructions, integration launch files and a `.repos` manifest for tools such as vcstool. Use branches for ongoing development or commit identifiers for reproducible versions. Git submodules are another option but require their own update workflow.

Exclude generated files such as `build/`, `install/`, `log/`, `.venv/`, `__pycache__/` and local measurement logs from the appropriate repository.

## Documentation responsibilities

| Document | Content |
| --- | --- |
| `README.md` | What the repository does and how to choose Python or ROS 2 |
| `docs/1_wiring.md` | Hardware identification, electrical connections and firmware upload |
| `docs/2_integration.md` | Cloning, workspace integration and Git synchronization |
| `docs/3_udev_rules.md` | Persistent Linux serial alias and permissions |

## References

- [ScioSense ENS160 datasheet](https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf)
- [colcon package discovery arguments](https://colcon.readthedocs.io/en/released/reference/discovery-arguments.html)
- [colcon workspace structure](https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html)

