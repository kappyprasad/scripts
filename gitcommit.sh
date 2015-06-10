#!/usr/bin/env sh

help="\
usage: $(basename $0) <comment>\n\
\n\
-v verbose\n\
-h help\n\
-t test\n\
-m commentt\n\
"

verbose=0
test=''
comment=''

while getopts vhtm opt
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
        m)
            comment=$OPTARG
            ;;
    esac
done

shift $((OPTIND-1))

if [ -z "$comment" ]
then
    comment=$(echo $*)
fi

if [ -z "$comment" ]
then
    echo "$help"
    exit 0
fi

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
            echo "$repo"
        fi

        lines=$(echo $(git status --porcelain | wc -l))
        if [ ! "$lines" = "0" ]
        then
            $test git commit -m "$comment"
        fi

        popd >/dev/null
    fi
done
