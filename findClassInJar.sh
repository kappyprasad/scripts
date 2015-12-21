#!/usr/bin/env bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



if [ "$1" == "" ]
then
    echo "usage: $0 <class>"
    exit 1
fi

if [ "$2" == "" ]
then
    find . -iname "*.jar" -exec $0 $1 {} \;
else
    if unzip -v $2 2>/dev/null | grep -i --color=auto "$1.*\.class" > /dev/null
    then
	echo $2
    fi
fi
