#!/bin/bash

for repo in *
do
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then
	    pushd "$repo" > /dev/null
	    pwd
	    git pull
	    popd > /dev/null
    fi
done


