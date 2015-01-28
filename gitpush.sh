#!/bin/bash

# bulk pusher

for repo in *
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd
        git push
        popd >/dev/null
    fi
done
