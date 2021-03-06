#!/usr/bin/env bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



args="$*"

if [ "$args" = "" ]
then
    echo "usage: "`basename $0`" [-v] <files>"
    exit 1
fi

if [ "$1" = "-v" ]
then
    svn propget svn:ignore
else
    svn propget svn:ignore > .svnignore
    for i in $*
    do
        i=$(echo $i | perl -pe 's|/$||;')
        echo $i >> .svnignore
    done
    sort -u .svnignore -o .svnignore
    svn propset svn:ignore -F .svnignore .
    rm .svnignore
fi
