#!/bin/bash 

# udev rules must be installed on host machine with USB device
# this enables executables that acceses USB devices to be ran without sudo

fn=/etc/udev/rules.d/51-blink1.rules 
if [ ! -e $fn ] ; then 
  cp ./udev-rules/51-blink1.rules $fn
fi 

sudo udevadm control --reload 
sudo udevadm trigger 