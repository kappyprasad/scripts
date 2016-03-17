#!/usr/bin/env bash

file="$1"

if [ ! -f "$file" ]
then
    echo "useage: $(basename $0) <zip>"
    exit 1
fi

leader=$(echo $file | cut -c -1)
#echo "leader=$leader"
if [ "$leader" = "/" ] || [ "$leader" = "~" ]
then
    source="$file"
else
    source="$(pwd)/$file"
fi

target="$(basename "$file").exploded"

#echo "source=$source"
#echo "target=$target"

if [ -d "$target" ]
then
    echo "$target already exists"
    exit 1
fi

mkdir "$target"
pushd "$target"
unzip -q "$source"
popd
