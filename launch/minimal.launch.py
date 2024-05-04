from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from os import getcwd
from os.path import join

## based on dumbot -->
## LINK src/dumbot_bringup/launch/minimal.launch.py
def generate_launch_description():

    # use gardenbot paramaters and configs
    xacro_file_path = join(getcwd(),
    "urdf", "roboclaw.urdf.xacro")

    robot_description = {"robot_description": Command(['xacro ', xacro_file_path])}

    # use gardenbot paramaters and configs
    robot_controllers_path = join(getcwd(),
    "params", "roboclaw_controllers.yaml")

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, robot_controllers_path],
        output="both",
    )
    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        remappings=[],
        output="both",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="both",
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diffbot_base_controller", "--controller-manager", "/controller_manager"],
        output="both",
    )

    nodes = [
        ros2_control_node,
        robot_state_pub_node,
        joint_state_broadcaster_spawner,
        robot_controller_spawner,
    ]

    return LaunchDescription(nodes)
