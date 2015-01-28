#!/bin/bash

echo=''

if [ "$1" = "-a" ]
then
    query="^( M|\?\?)"
else
    query="^( M)"
fi

for repo in *
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd

        git status --porcelain \
            | egrep "$query" \
            | cut -c 4- \
            | xargs -r -I FILE $echo git add "FILE"

        git status --porcelain
        popd >/dev/null
    fi
done


