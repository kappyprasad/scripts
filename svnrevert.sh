#!/usr/bin/env bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



echo=""

if [ "$*" = "" ] || [ "$*" = "-v" ]
then
    if [ "$1" = "-v" ]
    then
        echo="echo"
    fi
    svn status | perl -ne 'print "$1\n" if (/^[\?]\s+(\S.*)$/);' | xargs -n1 -I FILE $echo rm -vfr "FILE"
    svn status | perl -ne 'print "$1\n" if (/^[\!]\s+(\S.*)$/);' | xargs -n1 -I FILE $echo svn delete "FILE"
    svn status | perl -ne 'print "$1\n" if (/^[ADM]\s+(\S.*)$/);' | xargs -n1 -I FILE $echo svn revert --depth infinity "FILE"
else
    svn revert $*
fi
