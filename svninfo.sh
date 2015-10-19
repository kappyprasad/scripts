#!/usr/bin/env bash

#  tree -P '*.xsd' --prune

help="\
usage: $(basename $0) <file>\n\
\n\
-v        Verbose\n\
-h        Help\n\
-n name   name\n\
"

OPTERR=0

name=''
output=''

while getopts vhn: opt
do
    case $opt in
        v) 
            echo "verbose is on"
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        n) 
            name=$OPTARG
            ;;
    esac
done

shift $((OPTIND-1))

if [ -z "$name" ]
then
    echo -e "$help"
    exit 1
fi

file="$1"

if [ -z "$file" ]
then
    options="-n $name"
    echo "<html><body>" 
    find . -iname "$name" -exec $0 $options {} \;
    echo "</body></html>"
else
    if ! echo $file | grep "/target/" > /dev/null
    then
        file=$(echo $file | cut -c 3-)
        echo $file >&2
        url=$(svn info $file | perl -ne 'print "$1\n" if (/^URL: (.*)$/)');
        #base=$(echo $url | perl -pe "s|$file||")
        #echo $base
        echo "<a href='$url'>$file</a><br/>"
    fi
fi
