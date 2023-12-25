#!/bin/bash
set -e

# Set the default build type
BUILD_TYPE=RelWithDebInfo
echo "=== Starting build.sh ==="
colcon build \
        --base-path "/workspaces/bot2_ros2_workspace/src" \
        --merge-install \
        --symlink-install \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        -Wall -Wextra -Wpedantic
