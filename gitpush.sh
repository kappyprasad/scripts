#!/usr/bin/env bash

help="\
usage: $(basename $0) <repo>\n\
\n\
-v verbose\n\
-h help\n\
-a all everything\n\
-O all repos\n\
-B all branches\n\
-r recurse\n\
-o origin\n\
-b branch\n\
-t test only dont execute\n\
"

verbose=''
all=''
origins=''
branches=''
recurse=''
origin='origin'
branch='master'
test=''
echo=''

while getopts vhaOBro:b:t opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        a)
            all='-a'
            ;;
        O)
            origins='-O'
            ;;
        B)
            branches='-B'
            ;;
        r)
            recurse='-r'
            ;;
        o)
            origin=$OPTARG
            ;;
        b)
            branch=$OPTARG
            ;;
        t)
            test='-t'
            echo='echo'
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"

if [ -z "$repo" ] && [ "$recurse" = "-r" ]
then
    find . -name .git -and -type d -exec $0 \
         $verbose \
         $all \
         $origins \
         $branches \
         $recurse \
         $test \
         -o "$origin" \
         -b "$branch" \
         "{}" \
    \;
else
    if [ "$recurse" = "-r" ]
    then
        repo=$(dirname "$repo")
    else
        repo=.
    fi

    pushd "$repo" > /dev/null
    
    if [ "$verbose" = "-v" ]
    then
        horizontal.pl
        echo -e "\033[36m$repo\033[0m"
    fi

    if [ -d '.git' ]
    then
        if [ "$all" = "-a" ]
        then
            for origin in $(git remote)
            do
                if [ "$verbose" = "-v" ]
                then
                    horizontal.pl .
                    echo -e "\033[34m$origin\033[0m"
                fi
                $echo git push $origin $branch
            done
        else
            $echo git push $origin $branch
        fi
    else
        echo ".git not found" 1>&2
    fi
    
    popd >/dev/null
fi

