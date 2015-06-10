#!/bin/bash

if [ -d .git ]
then
    local=1
    repos=$(pwd)
else
    local=0
    repos=*
fi

for repo in $repos
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        if [ "$local" = "0" ]
        then
            echo $repo
        fi

	    git diff

        popd >/dev/null
    fi
done
