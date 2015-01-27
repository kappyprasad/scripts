#!/bin/bash

fetch="$1"

for repo in *
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd
	if [ "$fetch" = "-f" ]
	then
	    git fetch
	fi
        git status
        popd >/dev/null
    fi
done
