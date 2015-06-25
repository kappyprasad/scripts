#!/usr/bin/env sh

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
	    pushd "$repo" > /dev/null
        if [ -d ".git" ]
        then
            if [ "$local" = "0" ]
            then
                echo "\033[36m$repo\033[0m"
            fi
	    git pull
        fi
	    popd > /dev/null
    fi
done


