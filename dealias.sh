#!/usr/bin/env bash

a="$1"

if [ -z "$a" ]
then
    echo "usage: $(basename $0): <alias>" >&2
    exit 1
fi

b=$(alias "$a")
#echo $b

#everything after the first '
c=${b#*\'}
#echo $c

#everything before the last '
d=${c%\'*}
echo $d

