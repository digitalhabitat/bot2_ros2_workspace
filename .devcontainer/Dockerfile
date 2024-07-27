FROM althack/ros2:humble-dev 

# ** [Optional] Uncomment this section to install additional packages. **
#
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install --no-install-recommends <your-package-list-here> \
#    #
#    # Clean up
#    && apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get -y install --no-install-recommends \
   # MTM: joystick teleop test
   joystick jstest-gtk evtest \ 
   ros-humble-joy \
   ros-humble-joy-teleop \
   ros-humble-teleop-twist-joy \
   ros-humble-turtlesim \
   # MTM: roboclaw dev tools
   libserial-dev \
   ros-humble-differential \
   ros-humble-diff-drive-controller \
   ros-humble-joint-state-broadcaster \
   ros-humble-controller-manager \
   # MTM: RTK GNSS NTRIP Client Node (RTKLIB str2str)
   ros-humble-ntrip-client \
   # MTM: (RTKLIB str2str)
   rtklib \
   # MTM: RTK GNSS Reciever Device Node
   ros-humble-nmea-navsat-driver \
   # Global Positioning System - daemon
   gpsd \
   # MTM: connects to a GPSd server and broadcasts GPS fixes using the NavSatFix message plus more
   ros-humble-gpsd-client \
   ros-humble-gps-tools \
   ros-humble-gps-umd \ 
   # Basic Networking Tools
   netcat \
   net-tools \
   iproute2 \
   iputils-ping \
   # MTM: dev tools
    ros-humble-rqt-graph \
   # Clean up
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

# MTM: enable blink1 executable blink1-tool
ENV PATH=$PATH:/workspaces/bot2_ros2_workspace/src2/blink1-tool

# MTM: Adding label 
LABEL type="bot"

# Set up auto-source of workspace for ros user
ARG WORKSPACE
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc
