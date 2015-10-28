#!/usr/bin/env sh

help="\
usage: $(basename $0) <repos>\n\
\n\
-v verbose\n\
-h help\n\
-r recurse\n\
-o origin\n\
-b branch\n\
-s submodules\n\
-t test only dont execute\n\
"

verbose=''
recurse=''
all=''
origin='origin'
branch='master'
submodules=''
test=''
echo=''

while getopts vharso:b:t opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo -e "$help"
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
        s)
            submodules='-s'
            ;;
        t)
            test='-t'
            echo='echo'
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"

function gitpull {
    if [ "$submodules" = "-s" ]
    then
        $echo git pull --recurse-submodules $origin $branch
        $echo git submodule init
        $echo git submodule update --recursive
    else
        $echo git pull $origin $branch
    fi
}

if [ -z "$repo" ] && [ "$recurse" = "-r" ]
then
    options="$verbose $all $recurse $test $submodules -o $origin -b $branch"
    find . -name .git -and -type d -exec $0 $options "{}" \;
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
                    echo "\033[34m$origin\033[0m"
                fi
                
                gitpull
            done
        else
            gitpull
        fi
    fi
    
    popd >/dev/null
fi

