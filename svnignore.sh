#!/bin/bash

# $Date: 2014-03-11 19:20:01 +1100 (Tue, 11 Mar 2014) $
# $Revision: 9247 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/svnignore.sh $
# $Id: svnignore.sh 9247 2014-03-11 08:20:01Z david.edson $

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
        echo $i >> .svnignore
    done
    sort -u .svnignore -o .svnignore
    svn propset svn:ignore -F .svnignore .
    rm .svnignore
fi
