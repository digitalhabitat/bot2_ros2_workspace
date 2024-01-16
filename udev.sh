#!/bin/bash 

# Install udev rules on host machine with to enable executables
# that acceses USB devices to be ran without sudo

err() {
  echo "[ERROR] [$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# Check if running inside a Docker container
if [ "$(systemd-detect-virt --container)" == "docker" ]; then
  err "Running inside a Docker container."
  err "Installation Failed: This script is intended to be executed " \
  "on the host machine, not within a container. Execute it outside " \
  "the container environment to install udev rules properly."
  exit 1
fi

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    err "Please run this script with sudo or as root."
    exit 1
fi

# Define the source and destination directories
dir="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
dirSource="$dir/udev-rules"
dirTarget="/etc/udev/rules.d"

printf "Source Directory: $dirSource\n"
printf "Target Directory: $dirTarget\n\n"

# Check if the source directory exists
if [ ! -d "$dirSource" ]; then
    err "Source directory $dirSource does not exist."
    exit 1
fi

# Check if the destination directory exists
if [ ! -d "$dirTarget" ]; then
    err "Source directory $dirTarget does not exist."
    exit 1
fi

# cp "$dirSource"/*.rules "$dirTarget"

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

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=tty

printf "\nudev rules have been reloaded and triggered\n"