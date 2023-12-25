#!/bin/bash
set -e

echo "=== Starting test.sh ==="
echo "Working directory: $(pwd)"

if [ -f install/setup.bash ]; then source install/setup.bash; fi
colcon test --base-path "/workspaces/bot2_ros2_workspace/src" --merge-install
colcon test-result --verbose
