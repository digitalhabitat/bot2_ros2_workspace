import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def MotorControllerConnected():
    # Define emlid rtk serial device by alias
    SERIAL_DEVICE = "/dev/roboclaw"

    # Check if the serial device exists
    if os.path.exists(SERIAL_DEVICE):
        print(f"{bcolors.OKGREEN}Serial device {SERIAL_DEVICE} detected.{bcolors.ENDC}")
        return True
    else:
        print(f"{bcolors.WARNING}Serial device {SERIAL_DEVICE} is not detected.{bcolors.ENDC}")
        return False

def JoystickConnected():
    # Define emlid rtk serial device by alias
    SERIAL_DEVICE = "/dev/input/js0"

    # Check if the serial device exists
    if os.path.exists(SERIAL_DEVICE):
        print(f"{bcolors.OKGREEN}Serial device {SERIAL_DEVICE} detected.{bcolors.ENDC}")
        return True
    else:
        print(f"{bcolors.WARNING}Serial device {SERIAL_DEVICE} is not detected.{bcolors.ENDC}")
        return False



def generate_launch_description():

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

    gardenbot_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource('/workspaces/bot2_ros2_workspace/launch/minimal.launch.py')
    )

    ld = LaunchDescription()

    if MotorControllerConnected() and JoystickConnected():
        ld.add_action(LogInfo(msg="Starting auto_cell_str2str..."))
        ld.add_action(
            DeclareLaunchArgument(
                'joy_teleop_config_path',
                default_value=joy_teleop_config_path,
                description='Path to the joy_teleop config file'
            )
        )
        ld.add_action(joy_node)
        ld.add_action(joy_teleop)
        ld.add_action(gardenbot_bringup)
    else:
        ld.add_action(LogInfo(msg="Devices not connected."))

    return ld

