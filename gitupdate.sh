#!/bin/bash

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
	    pushd "$repo" > /dev/null
	    pwd
	    git pull | grep -v "Already up-to-date"
	    popd > /dev/null
    fi
done


