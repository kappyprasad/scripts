#!/bin/bash

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/svncheckout.sh $
# $Id: svncheckout.sh 7279 2013-12-12 14:22:40Z david.edson $

file=$1

if [ "$file" = "" ]
then
    echo "usage: $0 <file>"
    exit 1
fi

for r in `svn log $file | perl -ne 'print "$1\n" if (/^r(\d+)\s/);'`
do
    svn update -r $r $file
    mv $file $file.$r
done

svn update $file
