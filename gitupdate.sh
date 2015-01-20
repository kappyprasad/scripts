#!/bin/bash

for i in *
do
    if [ -d "$i" ]
    then
        pushd "$i" > /dev/null
        pwd
        git pull
        popd > /dev/null
    fi
done

