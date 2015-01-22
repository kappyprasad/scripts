#!/bin/bash

for i in *
do 
    if [ -d "$i" ]
    then 
        horizontal.pl
        pushd $i > /dev/null
        pwd
        git status
        popd >/dev/null
    fi
done
