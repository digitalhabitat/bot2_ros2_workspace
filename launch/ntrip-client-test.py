# Import necessary modules
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import yaml
import os

# This is a launch file to test the RTK GNSS device
# Depends on './config/ntrip_param.yaml' to provide login credentials to NTRIP caster

# ros-humble-ntrip-client
# https://github.com/LORD-MicroStrain/ntrip_client

# ros-humble-nmea-navsat-driver
# https://github.com/ros-drivers/nmea_navsat_driver/tree/ros2

def generate_launch_description():

    # Get file path string for .yaml config file
    yaml_file_path = os.path.join(os.getcwd(),
    'config/ntrip_client.yaml'
    )

    # Check if the file exists before attempting to open it
    if not os.path.exists(yaml_file_path):
        raise FileNotFoundError(f"File not found: {yaml_file_path}")

    # Open the yaml file 
    with open(yaml_file_path, 'r') as f:
        yaml_config = yaml.safe_load(f)
        #print(f'Loaded yaml_params: {yaml_params}')
        #print(f'Host: {yaml_params["ntrip_client"]["ros__parameters"]["host"]}')

        # Get list of key-value pairs
        param = yaml_config["ntrip_client"]["ros_parameters"]
        #for key, value in yaml_ntrip_param.items():
            #print(f'{key}: {value}')

    # Define default parameters for the Node
    default_params = {
        # Set the log level to debug
        'NTRIP_CLIENT_DEBUG': 'false',

        # Required parameters used to connect to the NTRIP server
        'host': param.get('host'),
        'port': param.get('port_single'),
        'mountpoint': param.get('mountpoint_single'),

        # If this is set to true, we will read the username and password and attempt to
        # authenticate. If not, we will attempt to connect unauthenticated
        'authenticate': True,

        # If authenticate is set to true, we will use these to authenticate with the server
        'username': param.get('username'),
        'password': param.get('password'),

        # Optional parameter that will set the NTRIP version in the 
        # initial HTTP request to the NTRIP caster
        'ntrip_version': '',

        # Whether to connect with SSL. cert, key,
        # and ca_cert options will only take effect if this is true
        'ssl': False,

        # If the NTRIP caster uses cert based authentication,
        # you can specify the cert and keys to use with these options
        'cert': '',
        'key': '',

        # If the NTRIP caster uses self signed certs,
        # or you need to use a different CA chain, specify the path to the file here
        'ca_cert': '',

        # Frame ID will be added to the RTCM messages published by this node
        'rtcm_frame_id': 'odom',

        # Optional parameters that will allow for longer or shorter NMEA messages.
        # Standard max length for NMEA is 82
        'nmea_max_length': 82,
        'nmea_min_length': 3,

        # Use this parameter to change the type of RTCM message published by the node
        # Supports "mavros_msgs" and "rtcm_msgs"
        'rtcm_message_package': 'rtcm_msgs',

        # Will affect how many times the node will attempt to reconnect before exiting,
        # and how long it will wait in between attempts when a reconnect occurs
        'reconnect_attempt_max': 10,
        'reconnect_attempt_wait_seconds': 5,

        #  How many seconds is acceptable in between receiving RTCM.
        # If RTCM is not received for this duration, the node will attempt to reconnect
        'rtcm_timeout_seconds': 4,
    }
    for key, value in default_params.items():
        print(f'{key}: {value}')

    # Generate a launch description for the ntrip client node
    ntrip_client_node = Node(
        package='ntrip_client',
        executable='ntrip_ros.py',
        name='ntrip_client_node',
        namespace='ntrip_client',
        output='screen',
        parameters=[default_params],
        # remappings=[('/ntrip_client/nmea', '/nmea')],
    )

    # Get file path string for .yaml config file
    config_file = os.path.join(os.getcwd(),
    "config", "nmea_serial_driver.yaml"
    )
    
    # Generate a launch description for a single serial driver
    driver_node = Node(
        package='nmea_navsat_driver',
        executable='nmea_serial_driver',
        output='screen',
        parameters=[config_file])

    # Add the Node to the LaunchDescription
    return LaunchDescription([ntrip_client_node])