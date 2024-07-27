#!/bin/bash

# Define emlid rtk serial device by alias
SERIAL_DEVICE="/dev/emlid_rtk"

# Check if the serial device exists
if [ -c "$SERIAL_DEVICE" ]; then
  echo "Serial device $SERIAL_DEVICE is detected."
  exit 0
else
  echo "Serial device $SERIAL_DEVICE is not detected."
  exit -1
fi