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

svn status | perl -ne 'print "$1\n" if (/^\!\s+(\S.*)$/);' | xargs -r -I FILE -d '\n\r' $echo svn remove FILE