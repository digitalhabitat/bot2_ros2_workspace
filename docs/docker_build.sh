#!/bin/bash

#TODO(MTM): Change label to `label=type=bot`
container_id=$(docker ps --filter "label=devcontainer.metadata" --filter status=running --format "{{.ID}}")

if [ -n "$container_id" ] && [ $(echo "$container_id" | wc -w) -eq 1 ]; then
    echo "Container ID: $container_id"
elif [ -z "$container_id" ]; then
    echo "Error: No containers match the criteria."
    exit 1
else
    echo "Error: Multiple containers match the criteria."
    exit 1
fi

docker exec -u ros -w /workspaces/bot2_ros2_workspace $container_id ./build.sh