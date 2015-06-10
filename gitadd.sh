#!/usr/bin/env sh

help="\
usage: $0 <files>\n\
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

        git status --porcelain \
            | egrep "$query" \
            | cut -c 4- \
            | xargs -n1 -I FILE $test git add "FILE"

        
        git status --porcelain

        popd >/dev/null
    fi
done


