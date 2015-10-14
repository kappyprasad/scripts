#!/usr/bin/env bash

svn="$1"

if [ -z "$svn" ]
then
    find . \( -name .svn -and -type d \) -exec $0 {} \;
else
    horizontal.pl
    pushd "$svn/.." > /dev/null
    pwd
    svn cleanup
    popd > /dev/null
fi
