# Building Notes

> [!INFO]
> Some ROS2 packages such as "roboclaw" may crash when they are built on a Raspberry Pi. The reason 
> behind this is because the pi will run out of swap memory during the colcon build process. 

https://gist.github.com/Myzhar/244dfc2bbb5d1f686865c0a86027567a#file-build_debug-sh
https://github.com/ROBOTIS-GIT/turtlebot3/issues/965#issuecomment-1631651554

## Checking Swap Memory

```bash
free -h
```

```bash
read -r total free <<< $(free -h | awk '/Swap:/ {print $2, $4}')
echo "Swap: $total(Total) $free(Free)"
```

## Increasing Swap Memory on Raspberry Pi 4

Run this command host environment not inside the container.

```bash
# Check current swap size (Ras)
sudo swapon --show

# Disable swap
sudo dphys-swapfile swapoff

# Edit configuration file
sudo nano /etc/dphys-swapfile
# Look for the line CONF_SWAPSIZE and change the value (e.g., CONF_SWAPSIZE=2048)

# Save and exit

# Update configuration
sudo dphys-swapfile setup

# Enable swap
sudo dphys-swapfile swapon

# Verify new swap size
sudo swapon --show
```

## Building from host terminal

Get the ID of the currently running ROS workspace container.

```bash
#TODO(MTM): Change label to `label=type=bot`
docker ps --filter "label=devcontainer.metadata" --filter status=running --format "{{.ID}}"
```

Execute the `./build.sh` script via the docker command

```bash
docker exec -u ros -w /workspaces/bot2_ros2_workspace $container_id ./build.sh
```

The reason to do it this way is because the vscode gui will timeout and disrupt the logging when
you attempt to build the package within vscode remote development gui.