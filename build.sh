#!/bin/bash
set -e

# https://gist.github.com/Myzhar/244dfc2bbb5d1f686865c0a86027567a#file-build_debug-sh

# Set the default build type
BUILD_TYPE=RelWithDebInfo
echo -e "=== Starting build.sh ==="
echo "Working directory: $(pwd)"

colcon build \
        --base-path "./src" \
        --packages-select "roboclaw" \
        --merge-install \
        --symlink-install \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        --parallel-workers $(nproc)
        -Wall -Wextra -Wpedantic 
