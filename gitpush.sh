#!/bin/bash

# bulk pusher

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
        if git status | grep "use \"git push\" to publish your local commits" >/dev/null
        then
            git push
        fi
        popd >/dev/null
    fi
done
