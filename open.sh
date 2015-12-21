#!/usr/bin/env bash

path=$1

if [ ! -f "$path/Info.plist" ]
then
    echo "no Info.plist found in $path"
    exit
fi

open $(plutil -key CFBundleIdentifier "$path/Info.plist")
