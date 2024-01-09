# Import necessary modules
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import yaml
import os

# TODO: Determine how to send RTCM messages through ROS topics
# The ntrip-client is working fine however there is an issue subscribing to RTCM messages for the
# receiver. At the moment I am not sure there is a ROS2 driver/node that interfaces with a
# "U-blox NEO-M8T" (Emlid Reach) receiver with parameters to support DGNSS.

# This is a launch file to test the RTK GNSS device
# Depends on './config/ntrip_param.yaml' to provide login credentials to NTRIP caster

# ros-humble-ntrip-client
# https://github.com/LORD-MicroStrain/ntrip_client

# FIXME: This node does not support RTCM messages. Find another package that does.
# ros-humble-nmea-navsat-driver
# https://github.com/ros-drivers/nmea_navsat_driver/tree/ros2
# required: sudo pip3 install transforms3d

def generate_launch_description():

    # Get file path string for .yaml config file
    default_config = os.path.join(os.getcwd(),
    "config", "ntrip_client_node.yaml"
    )

    # NTRIP client login secrets
    ntrip_login = os.path.join(os.getcwd(),
    "config", "ntrip_login.yaml"
    )

    # Open the yaml file 
    with open(ntrip_login, 'r') as f:
        yaml_config = yaml.safe_load(f)
        login_param = yaml_config["ntrip_client_node"]["login"]

    # Define login parameters for the ntrip_client_node
    login_params = {
        'host': login_param.get('host'),
        'port': login_param.get('port_single'),
        'mountpoint': login_param.get('mountpoint_single'),
        'authenticate': True,
        'username': login_param.get('username'),
        'password': login_param.get('password')
    }

    # Generate a launch description for the ntrip client node
    ntrip_client_node = Node(
        package='ntrip_client',
        executable='ntrip_ros.py',
        name='ntrip_client_node',
        namespace='ntrip_client',
        output='screen',
        parameters=[default_config,login_params],
        # remappings=[('/ntrip_client/nmea', '/nmea')],
    )

    # Get file path string for .yaml config file
    config_file = os.path.join(os.getcwd(),
    "config", "nmea_serial_driver.yaml"
    )
    
    # Generate a launch description for a single serial driver
    nmea_driver_node = Node(
        package='nmea_navsat_driver',
        executable='nmea_serial_driver',
        output='screen',
        parameters=[config_file])

    # Add the Node to the LaunchDescription
    return LaunchDescription([
        ntrip_client_node,
        nmea_driver_node])