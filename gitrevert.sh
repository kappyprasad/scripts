#!/bin/bash

read -p "are you sure (yes/no) ? " sure

if [ "$sure" != "yes" ]
then
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
	    pushd "$repo" > /dev/null
	    pwd
	    git status --porcelain | cut -c 4- | xargs -n1 git checkout
	    popd > /dev/null
    fi
done
