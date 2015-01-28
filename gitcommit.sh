#!/bin/bash

# bulk committer, assumes items already added to index

comment="$*"

if [ -z "$comment" ]
then
    echo "usage: $0 <comment>"
    exit 1
fi

for repo in *
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        pwd
        git commit -m "$comment"
        popd >/dev/null
    fi
done
