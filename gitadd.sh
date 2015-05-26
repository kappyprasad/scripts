#!/bin/bash

echo=''

if [ "$1" = "-a" ]
then
    query="^( M|\?\?)"
else
    query="^( M)"
fi

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

        git status --porcelain \
            | egrep "$query" \
            | cut -c 4- \
            | xargs -n1 -I FILE $echo git add "FILE"

        git status --porcelain
        popd >/dev/null
    fi
done


