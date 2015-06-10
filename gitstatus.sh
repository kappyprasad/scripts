#!/usr/bin/env sh

help="\
usage: $(basename $0) <files>\n\
\n\
-v verbose\n\
-h help\n\
-f fetch\n\
"

verbose=0
fetch=0

while getopts vhf opt
do
    case $opt in
        v) 
            verbose=1
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        f)
            fetch=1
            ;;
    esac
done

shift $((OPTIND-1))

if [ -d .git ]
then
    repos=$(pwd)
else
    repos=*
fi

for repo in $repos
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null
        if [ "$verbose" = "1" ]
        then
            pwd
        fi

	    if [ "$fetch" = "1" ]
	    then
            if [ "$verbose" = "1" ]
            then
                echo "git fetch"
            fi
	        git fetch
	    fi

        git status --porcelain $*

        popd >/dev/null
    fi
done
