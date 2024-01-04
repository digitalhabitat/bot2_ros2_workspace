#!/bin/bash 

# udev rules must be installed on host machine with USB device
# this enables executables that acceses USB devices to be ran without sudo

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo or as root."
    exit 1
fi

# Define the source and destination directories
dirSource="/home/bot/bot2_ros2_workspace/udev-rules"
dirTarget="/etc/udev/rules.d"

printf "Source Directory: $dirSource\n"
printf "Target Directory: $dirTarget\n\n"

# Check if the source directory exists
if [ ! -d "$dirSource" ]; then
    echo "Source directory $dirSource does not exist."
    exit 1
fi

# Check if the destination directory exists
if [ ! -d "$dirTarget" ]; then
    echo "Source directory $dirTarget does not exist."
    exit 1
fi

# Loop through files in source directory
for file in $dirSource/*.rules; do

    # Filter out non-matching glob https://mywiki.wooledge.org/BashPitfalls#line-57
    [ -e "$file" ] || continue

    # Extract the filename without the path
    filename=$(basename "$file")

    # Check if the file exists in target directory
    if [ -e "$dirTarget/$filename" ]; then
        echo "File $filename is already present in $dirTarget."
    else
        # If the file doesn't exist, copy it to directory B
        cp "$file" "$dirTarget"
        echo "File $filename copied to $dirTarget."
    fi
done

sudo udevadm control --reload 
sudo udevadm trigger 

printf "\nudev rules have been reloaded and triggered\n"