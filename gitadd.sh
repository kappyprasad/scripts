#!/bin/bash

echo=""

if [ "$1" = "-v" ]
then
    echo=echo
fi

git status --porcelain | egrep "^( M|\?\?)" | cut -c 4- | xargs -r -I FILE $echo git add "FILE"


