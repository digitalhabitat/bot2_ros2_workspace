#!/bin/bash
set -e

# Set the default build type
BUILD_TYPE=RelWithDebInfo
colcon build \
        --merge-install \
        --symlink-install \
        --packages-select blink1_ros2 \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        -Wall -Wextra -Wpedantic
