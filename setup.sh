#!/bin/bash
set -e

echo "=== Starting setup.sh ==="
echo "$(pwd)"
vcs import < src/ros2.repos src
sudo apt-get update
rosdep update
rosdep install --from-paths src --ignore-src -y
