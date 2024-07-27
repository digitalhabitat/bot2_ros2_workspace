import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart

from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def GpsConnected():
    # Define emlid rtk serial device by alias
    SERIAL_DEVICE = "/dev/emlid_rtk"

    # Check if the serial device exists
    if os.path.exists(SERIAL_DEVICE):
        print(f"Serial device {SERIAL_DEVICE} is detected.")
        return True
    else:
        print(f"Serial device {SERIAL_DEVICE} is not detected.")
        return False

def generate_launch_description():

    # Get file path string for str2str secret parameters file
    env_rtk = "/workspaces/bot2_ros2_workspace/config/.env.rtk"

    # Get file path for 
    detect_emlid_cnx = '/workspaces/bot2_ros2_workspace/scripts/emlid-detect.sh'

    check_serial_device = ExecuteProcess(
        cmd=[detect_emlid_cnx],
        name='emlid_detect',
        output='screen'
    )

    # single site str2str command
    # dotenvx run -f ./config/.env.rtk -- sh -c 'echo "ntrip://$NT_USER:$NT_PASSWORD@$NT_HOSTNAME:$NT_PORT_SINGLE/$NT_ENDPOINT_SINGLE"'
    single_site_str2str = ExecuteProcess(
        cmd = ["dotenvx",
               "run",
                "-f", env_rtk,
                "--",
                "sh -c",
                "'str2str ",
                "-in ntrip://$NT_USER:$NT_PASSWORD@$NT_HOSTNAME:$NT_PORT_SINGLE/$NT_ENDPOINT_SINGLE ",
                "-out serial://emlid_rtk:115200#9123'"],
        name='str2str',
        shell=True,
        output='screen'
    )

    # automatic cells str2str command
    # dotenvx run -f ./config/.env.rtk -- sh -c 'echo "ntrip://$NT_USER:$NT_PASSWORD@$NT_HOSTNAME:$NT_PORT_AUTO/$NT_ENDPOINT_AUTO"'
    if False: '''
    dotenvx run -f ./config/.env.rtk -- sh -c 'str2str \
    -in ntrip://$NT_USER:$NT_PASSWORD@$NT_HOSTNAME:$NT_PORT_AUTO/$NT_ENDPOINT_AUTO \
    -out serial://emlid_rtk:115200#9123 -b 1'
    '''
    auto_cell_str2str = ExecuteProcess(
        cmd = ["dotenvx",
               "run",
                "-f", env_rtk,
                "--",
                "sh -c",
                "'str2str ",
                "-in ntrip://$NT_USER:$NT_PASSWORD@$NT_HOSTNAME:$NT_PORT_AUTO/$NT_ENDPOINT_AUTO ",
                "-out serial://emlid_rtk:115200#9123 ",
                "-b 1'"], # relay back messages from output str to input str [number] (required for automatic cells)
        name='str2str',
        shell=True,
        output='screen'
    )

    # gpsd server
    # gpsd -N -S 9234 tcp://localhost:9123
    gpsd_foreground = ExecuteProcess(
        cmd = ["gpsd",
               "-N",                     # don't go into background
               "-S 9234",               # set port for daemon, default 2947
               "tcp://localhost:9123"], # connect to str2str Output Received Stream
    )

    # gpsd client ROS node
    # https://github.com/swri-robotics/gps_umd/blob/ros2-devel/gpsd_client/launch/gpsd_client-launch.py
    if False: '''
    ros2 run rclcpp_components component_container

    ros2 component load /ComponentManager gpsd_client gpsd_client::GPSDClientComponent \
    --node-name gpsd_client_composed_node --param host:=localhost --param port:=9234 \
    --param use_gps_time:=false --param check_fix_by_variance:=false --param frame_id:=gps \
    --param publish_rate:=1
    '''
    gpsd_client_container = ComposableNodeContainer(
        name='gpsd_client_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='gpsd_client',
                plugin='gpsd_client::GPSDClientComponent',
                name='gpsd_client_composed_node',
                parameters=[{
                    'host': 'localhost',
                    'port': 9234,
                    'use_gps_time': False,
                    'check_fix_by_variance': False,
                    'frame_id': 'gps',
                    'publish_rate': 1
                }]
            )
        ],
        output='screen',
    )

    # Event handler to start gpsd_foreground 8.0 seconds after str2str_auto starts
    cond_gpsd_foreground = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=auto_cell_str2str,
            on_start=[
                TimerAction(
                    period=8.0,
                    actions=[gpsd_foreground]
                )
            ]
        )
    )

    # Event handler to start gpsd_client_container 10 seconds after gpsd_foreground starts
    cond_gpsd_client_container= RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=gpsd_foreground,
            on_start=[
                TimerAction(
                    period=10.0,
                    actions=[gpsd_client_container]
                )
            ]
        )
    )



    ld = LaunchDescription()

    if GpsConnected():  # Check if GPS is detected
        ld.add_action(LogInfo(msg="Starting auto_cell_str2str..."))
        ld.add_action(auto_cell_str2str)
        ld.add_action(cond_gpsd_foreground)
        ld.add_action(cond_gpsd_client_container)
    else:
        ld.add_action(LogInfo(msg="GPS device not connected."))

    return ld
