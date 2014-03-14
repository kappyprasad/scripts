#!/bin/bash

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
