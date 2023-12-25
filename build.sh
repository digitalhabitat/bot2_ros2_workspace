#!/bin/bash
set -e

# Set the default build type
BUILD_TYPE=RelWithDebInfo
echo -e "=== Starting build.sh ==="
echo "Working directory: $(pwd)"

colcon build \
        --base-path "./src" \
        --merge-install \
        --symlink-install \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        -Wall -Wextra -Wpedantic
