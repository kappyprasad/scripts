#!/usr/bin/env bash

echo=""
commit=""

usage="\
usage: $(basename $0) \n\
    -h         help\n\
    -v         verbose mode\n\
    -t         test only, don't execute\n\
    -c         commit changes\n\
"

while getopts vhtc opt
do
    case $opt in
        v) 
            echo "verbose is on"
            ;;
        h) 
            echo -e $usage
            exit 0
            ;;
        t) 
            echo="-t"
            ;;
        c) 
            commit="-c"
            ;;
    esac
done

shift $((OPTIND-1))

target="$1"

if [ -z "$target" ]
then
    find . \( -name target -and -type d \) -exec $0 $commit $echo "{}" \;
else
    horizontal.pl
    pushd $(dirname "$target")
    if [ ! -z "$echo" ]
    then
        echo="echo"
    fi
    $echo svn remove target
    $echo svnignore.sh target
    if [ "$commit" == "-c" ]
    then
        $echo svn commit -m 'removing target' . target
    fi
    popd > /dev/null
fi

    
