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
        if [ "$local" = "0" ]
        then
            echo -e "\033[34m$repo\033[0m"
        fi

	    git pull

	    popd > /dev/null
    fi
done


