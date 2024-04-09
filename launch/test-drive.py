from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    # // TODO: Add script to detect /dev/roboclaw and usb controller
    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[{
            'dev': '/dev/input/js0',
            'deadzone': 0.05,
            'autorepeat_rate': 0.5
        }]
    )

    joy_teleop_config_path = LaunchConfiguration(
        'joy_teleop_config_path',
        default='/workspaces/bot2_ros2_workspace/config/teleop_joy_irl.yaml')

    joy_teleop = Node(
        package='joy_teleop',
        executable='joy_teleop',
        parameters=[joy_teleop_config_path]
    )

    dumbot_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource('/workspaces/bot2_ros2_workspace/src/dumbot_bringup/launch/minimal.launch.py')
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'joy_teleop_config_path',
            default_value=joy_teleop_config_path,
            description='Path to the joy_teleop config file'
        ),
        joy_node,
        joy_teleop,
        dumbot_bringup
    ])

