#!/usr/bin/env bash

help="\
usage: $(basename $0) <repos>\n\
\n\
-v verbose\n\
-h help\n\
-r recurse\n\
-O all origins\n\
-B all branches\n\
-a all everything\n\
-o origin\n\
-b branch\n\
-t test only dont execute\n\
"

verbose=''
recurse=''
all_everything=''
all_origins=''
all_branches=''
origin='origin'
branch='master'
test=''
echo=''

while getopts vhaOBro:b:t opt
do
    case $opt in
        v) verbose='-v';;
        h) echo -e "$help"; exit 0;;
        r) recurse='-r';;
        O) all_origins='-O';;
        B) all_branches='-B';;
        a) all_everything='-a';;
        o) origin=$OPTARG;;
        b) branch=$OPTARG;;
        t) test='-t'; echo='echo';;
        \?)
            # everything else is invalid
            echo -e "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"

if [ -z "$repo" ] && [ "$recurse" = "-r" ]
then
    find . -name .git -and -type d -exec $0 \
         $verbose \
         $all_everything \
         $all_origins \
         $all_branches \
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

        origins=()
        if [ "$all_everything" = "-a" ] || [ "$all_origins" = "-O" ]
        then
            origins=($(git remote))
        else
            origins=($origin)
        fi

        branches=()
        if [ "$all_everything" = "-a" ] || [ "$all_branches" = "-B" ]
        then
            branches=($(git branch | cut -c 3-))
        else
            branches=($branch)
        fi
        
        for o in ${origins[@]}
        do
            for b in ${branches[@]}
            do
                if [ "$verbose" = "-v" ]
                then
                    horizontal.pl .
                    echo -e "\033[34m$o->$b\033[0m"
                fi
                $echo git pull $o $b
            done
        done
    fi
    
    popd >/dev/null
fi

