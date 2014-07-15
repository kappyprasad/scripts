#!/bin/bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



echo=""

if [ "$1" = "-v" ]
then
    echo=echo
fi

if [ "$1" = "" ]
then
    svn status | perl -ne 'print "$1\n" if (/^\?\s+(\S.*)$/);' | xargs -r -I FILE -d '\n\r' $echo svn --parents add "FILE"
else
    svn add $*
fi
