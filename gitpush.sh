#!/bin/bash

# bulk pusher

for repo in *
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd
        lines=$(git status --porcelain | wc -l)
        if [ ! "$lines" = "0" ]
        then
            git push
        fi
        popd >/dev/null
    fi
done
