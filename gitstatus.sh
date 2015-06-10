#!/bin/bash

fetch="$1"

if [ -d .git ]
then
    verbose=0
    repos=$(pwd)
else
    verbose=1
    repos=*
fi

for repo in $repos
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        if [ "$verbose" = "1" ]
        then
            pwd
        fi

	    if [ "$fetch" = "-f" ]
	    then
	        git fetch
	    fi

        git status --porcelain

        popd >/dev/null
    fi
done
