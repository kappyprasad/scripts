#!/bin/bash

echo=""

if [ "$1" = "-v" ]
then
    echo=echo
fi

if [ "$1" = "-a" ]
then
    query="^( M|\?\?)"
else
    query="^( M)"
fi


git status --porcelain | egrep "$query" | cut -c 4- | xargs -r -I FILE $echo git add "FILE"


