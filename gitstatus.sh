#!/usr/bin/env sh

help="\
usage: $(basename $0) <repos...>\n\
\n\
-v verbose\n\
-h help\n\
-f fetch\n\
"

verbose=''
fetch=''

while getopts vhf opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        f)
            fetch="-f"
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"
if [ -z "$repo" ]
then
    find . -name .git -and -type d -exec $0 $verbose $fetch {} \;
else
    repo=$(dirname $repo)
    pushd $repo > /dev/null

    if [ "$verbose" = "-v" ]
    then
        horizontal.pl
        echo "\033[36m$repo\033[0m"
    fi

    if [ "$fetch" = "-f" ] 
    then
        git fetch
    fi
    git status --porcelain | grep -v "^?"
    
    popd >/dev/null
fi

