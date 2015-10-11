#!/usr/bin/env sh

help="\
usage: $(basename $0) <repo>\n\
\n\
-v verbose\n\
-h help\n\
-a all repos\n\
-r recurse\n\
-o origin\n\
-b branch\n\
-t test only dont execute\n\
"

verbose=''
all=''
recurse=''
origin='origin'
branch='master'
test=''
echo=''

while getopts vharo:b:t opt
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
    options="$verbose $all $recurse $test -o $origin -b $branch"
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
                    echo "\033[34m$origin\033[0m"
                fi
                $echo git push $origin $branch
            done
        else
            $echo git push $origin $branch
        fi
    fi
    
    popd >/dev/null
fi

