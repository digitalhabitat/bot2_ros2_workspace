from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # TODO: Add script to detect /dev/roboclaw and usb controller
    # NOTE: The repciprocal of 'autorepeat_rate' must be less than cmd_vel_timeout (see LINK)
    # 1/autorepeat_rate must be less than cmd_vel_timeout
    # `autorepeat_rate` is the frequency of duplicate consecutive joy_node data.
    # 1/autorepate_rate is the time duration between published duplicate consecutive joy_node data.
    # `cmd_vel_timeout` is the time duration the motor controller must receive a command before it
    # automatically stops
    # LINK - params/roboclaw_controllers.yaml
    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[{
            'dev': '/dev/input/js0',
            'deadzone': 0.05,
            'autorepeat_rate': 3.0
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

    return LaunchDescription([
        DeclareLaunchArgument(
            'joy_teleop_config_path',
            default_value=joy_teleop_config_path,
            description='Path to the joy_teleop config file'
        ),
        joy_node,
        joy_teleop
    ])

