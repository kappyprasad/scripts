#!/usr/bin/env bash

a="$1"

if [ -z "$a" ]
then
    echo "usage: $(basename $0): <alias>" >&2
    exit 1
fi

b=$(alias "$a")
#echo $b

c=${b#*\'}
#echo $c

d=${c%\'*}
echo $d

