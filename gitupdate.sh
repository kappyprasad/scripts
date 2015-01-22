#!/bin/bash

repo="$*"

if [ -z "$repo" ]
then
    find . -name .git -exec $0 "{}" \;
else
    dir=$(echo $repo | sed -e 's/.git$//')
    horizontal.pl
    pushd "$dir" > /dev/null
    pwd
    git pull
    popd > /dev/null
fi


