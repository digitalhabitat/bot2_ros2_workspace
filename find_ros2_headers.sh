#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <ros2-package-name>"
    exit 1
fi

pkg_name=$1
echo pakage: $pkg_name
prefix="$(ros2 pkg prefix "$pkg_name")"
echo prefix: $prefix
path=$prefix/include/$pkg_name/
echo path: $path

hpp_result=$(find "$path" -name "*.hpp" -not -path "*detail*")
h_result=$(find "$path" -name "*.h" -not -path "*detail*" -not -name "rosidl*")
echo "$hpp_result"
echo "$h_result"

trmd_hpp_result=${hpp_result//"$path"/}
trmd_h_result=${h_result//"$path"/}
echo "$trmd_hpp_result"
echo "$trmd_h_result"


