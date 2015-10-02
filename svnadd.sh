#!/bin/bash

echo=""

if [ "$1" = "-v" ]
then
    echo=echo
fi

svn status | perl -ne 'print "$1\n" if (/^\?\s+(\S.*)$/);' | xargs -n1 -I FILE $echo svn --parents add "FILE"
