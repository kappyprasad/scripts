#!/usr/bin/env bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


i="$*"

if [ ! -f "$i" ]
then
    echo "usage $0: <twx/zip>"
    exit 1
fi

if [ -d "$i.exploded" ]
then
    echo "$i already extracted"
    exit 1
fi

if echo "$i" | grep ".zip$" > /dev/null
then
    echo -ne "    "
fi

echo "$i"
mkdir -p "$i.exploded"
pushd "$i.exploded" > /dev/null
unzip -qo "../$i"

#pushd objects > /dev/null
#cleanChars.sh *.xml
#popd > /dev/null

if [ -d files ]
then
    pushd files > /dev/null
    for f in */*
    do
        if file $f | grep "Zip archive data" > /dev/null
	    then
	        unzip -v $f 2>/dev/null > $f.jar.log
	    fi
        if file $f | grep "ASCII" > /dev/null
	    then
	        cat -v $f > $f.txt
	    fi
    done
    popd > /dev/null
fi

if [ -d toolkits ]
then
    echo "  toolkits"
    pushd toolkits > /dev/null
    for t in *.zip
    do
        $0 "$t"
    done
    popd > /dev/null
fi
popd > /dev/null


