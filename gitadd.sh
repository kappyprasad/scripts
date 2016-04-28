#!/usr/bin/env bash

help="\
usage: $(basename $0) <files>\n\
\n\
-v verbose\n\
-h help\n\
-t test\n\
-d delete\n\
-a add\n\
"

verbose=0
test=''
matchers=('.M')

while getopts vhtda opt
do
    case $opt in
        v) 
            verbose=1
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        t)
            test='echo '
            ;;
        d) 
            matchers+=('.D')
            ;;
        a) 
            matchers+=('\?\?')
            ;;
    esac
done

shift $((OPTIND-1))

function join { 
    local IFS="$1" 
    shift
    echo "$*" 
}

query=$(join \| ${matchers[@]} )

if [ "$verbose" = "1" ]
then
    echo "matchers=$matchers"
    echo "query=$query"
fi

for git in $*
do
    $test git add $git
done

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
        pushd "$repo" > /dev/null

        if [ ! -d .git ]
        then
            echo "not in root of git tree"
            exit 1
        fi

        if [ "$local" = "0" ] || [ "$verbose" = "1" ]
        then
            echo -e "\033[36m$repo\033[0m"
        fi

        git status --porcelain \
            | egrep "$query" \
            | cut -c 4- \
            | perl -pe 's/ ->.*$//' \
            | xargs -n1 -I FILE $test git add "FILE"

        
        git status --porcelain

        popd >/dev/null
    fi
done


