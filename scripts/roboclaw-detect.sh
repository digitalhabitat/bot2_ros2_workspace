#!/bin/bash

# Define basic mirco roboclaw serial device by alias
SERIAL_DEVICE="/dev/roboclaw"

# Check if the serial device exists
if [ -c "$SERIAL_DEVICE" ]; then
  echo "Serial device $SERIAL_DEVICE is detected."
  exit 1
else
  echo "Serial device $SERIAL_DEVICE is not detected."
  exit -1
fi