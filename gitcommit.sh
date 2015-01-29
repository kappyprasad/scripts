#!/bin/bash

# bulk committer, assumes items already added to index

argument="$1"
comment="$2"

if [ -z "$*" ]
then
    echo "usage: $0 <comment>"
    exit 1
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
        lines=$(git status --porcelain | wc -l)
        if [ ! "$lines" = "0" ]
        then
            if [ "$argument" = "-m" ]
            then
                git commit -m "$comment"
            else
                git commit -m "$argument"
            fi
        fi
        popd >/dev/null
    fi
done
