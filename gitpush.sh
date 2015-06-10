#!/usr/bin/env sh

help="\
usage: $(basename $0)\n\
\n\
-v verbose\n\
-h help\n\
"

verbose=0

while getopts vh opt
do
    case $opt in
        v) 
            verbose=1
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
    esac
done

shift $((OPTIND-1))

if [ -d .git ]
then
    local=1
    repos=$(pwd)
else
    local=0
    repos=*
fi

for repo in $repos
do 
    if [ -d "$repo" ] && [ ! "$repo" = "." ]
    then 
        pushd $repo > /dev/null

        if [ "$local" = "0" ] || [ "$verbose" = "1" ]
        then
            echo $repo
        fi

        if git status | grep "use \"git push\" to publish your local commits" >/dev/null
        then
            git push
        fi

        popd >/dev/null
    fi
done
