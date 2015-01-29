#!/bin/bash

fetch="$1"

if [ -d .git ]
then
    repos=$(pwd)
else
    repos=*
fi

for repo in $repos
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd
	    if [ "$fetch" = "-f" ]
	    then
	        git fetch
	    fi
        git status --porcelain
        popd >/dev/null
    fi
done
