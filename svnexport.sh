#!/bin/bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


file="$1"

if [ "$file" == "" ]
then
    echo "usage: $0 <file>"
    exit
fi

if svn status -v $file | wc -l | grep "^0" > /dev/null
then
    echo "not an svn file"
    exit
fi

for i in `svn log "$file" | perl -ne 'print "$1\n" if (/^(r\d+)\s/);'`
do 
    horizontal.pl
    svn update -r $i $file
    mv -v $file $file.$i
done

horizontal.pl
svn update $file

