from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("port", default_value="/dev/ens160"),
        DeclareLaunchArgument("baud_rate", default_value="9600"),
        Node(
            package="ens160_air_quality_ros",
            executable="air_quality_node",
            name="air_quality_node",
            output="screen",
            parameters=[{
                "port": LaunchConfiguration("port"),
                "baud_rate": ParameterValue(
                    LaunchConfiguration("baud_rate"), value_type=int
                ),
            }],
        ),
    ])
