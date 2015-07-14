#!/usr/bin/env bash

target="$1"

if [ -z "$target" ]
then
    echo "usage $(basename $0): <targetDir>"
    exit 1
fi

resource="$2"

if [ -z "$resource" ]
then
    find . -type d -exec $0 "$target" "{}" \;
else
    if [ ! -e "$target/$resource" ]
    then
        echo "$resource"
    fi
fi
