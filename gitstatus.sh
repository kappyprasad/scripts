#!/bin/bash

for i in *
do 
    if [ -d "$i" ]
    then 
        pushd $i > /dev/null
        pwd
        horizontal.pl
        git status
        popd >/dev/null
    fi
done
