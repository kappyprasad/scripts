#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v         Verbose\n\
-h         Help\n\
-b backup  directory\n\
-s source  directory to clean\n\
-c compare file to test for removal\n\
"

OPTERR=0

verbose=''
current_dir=''
backup_dir=''
test_target=''

while getopts vhb:s:c: opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        b)
            backup_dir=$OPTARG
            ;;
        s)
            current_dir=$OPTARG
            ;;
        c)
            test_target=$OPTARG
            ;;
        \?)
            echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

if [ -z "$backup_dir" ]
then
    echo "$help"
    exit 1
fi

if [ -z "$current_dir" ]
then
    current_dir=$(pwd)
    test_target=""
fi

if [ "$backup_dir" = "$current_dir" ]
then
    echo "Cant backup to the same target"
    exit 1
fi

if [ "$test_target" = "" ]
then
    pushd "$backup_dir" >/dev/null
    options="$verbose -b \"$backup_dir\" -s $current_dir"
    find . ! -name '.' -exec $0 $options -c {} \; 2>/dev/null
else
    test_target=$(echo "$test_target" | perl -pe 's|^./||')
    
    if [ -e "$backup_dir/$test_target" ] \
    && [ ! -e "$current_dir/$test_target" ]
    then
        echo "-$test_target"
        rm -fr "$backup_dir"/"$test_target"
    fi
fi
