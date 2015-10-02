#!/usr/bin/env sh

help="\
usage: $(basename $0) <repos...>\n\
\n\
-v verbose\n\
-h help\n\
-f fetch\n\
-r recurse\n\
"

verbose=''
fetch=''
recurse=''

while getopts vhfr opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo -e "$help"
            exit 0
            ;;
        f)
            fetch="-f"
            ;;
        r)
            recurse="-r"
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"

if [ -z "$repo" ] && [ "$recurse" = "-r" ]
then
    options="$verbose $fetch $recurse"
    find . -name .git -and -type d -exec $0 $options {} \;
else
    if [ "$recurse" = "-r" ]
    then
        repo=$(dirname $repo)
    else
        repo=.
    fi

    pushd $repo > /dev/null

    if [ "$verbose" = "-v" ]
    then
        if ! git status --porcelain | grep -v "^?" | wc -l | grep "^\s*0\s*$" > /dev/null
        then
            horizontal.pl
            echo "\033[36m$repo\033[0m"
        fi
    fi

    if [ "$fetch" = "-f" ] 
    then
        git fetch
    fi
    git status --porcelain | grep -v "^?"
    
    popd >/dev/null
fi

