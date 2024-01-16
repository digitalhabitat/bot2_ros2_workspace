#!/bin/bash
set -e

# See // LINK docs/building-notes.md

# Set the default build type
BUILD_TYPE=RelWithDebInfo
PARALLEL_WORKERS=1
echo -e "=== Starting build.sh ==="
echo "Working directory: '$(pwd)'"
echo "User: '$(whoami)'"
echo "$(free -h | awk '/Swap:/ {printf "Swap: %s(Total) %s(Free)\n", $2, $4}')"
echo "Parallel workers: $PARALLEL_WORKERS" 

# Set parallel workers to 1 to prevent from running out of swap memory on Raspberry Pi

colcon build \
        --base-path "./src" \
        --packages-select "roboclaw" \
        --merge-install \
        --symlink-install \
        --parallel-workers $PARALLEL_WORKERS \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        -Wall -Wextra -Wpedantic
