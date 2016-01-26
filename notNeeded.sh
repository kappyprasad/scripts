#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v         Verbose\n\
-h         Help\n\
-b backup  directory\n\
-c current directory\n\
-t test    file to remove\n\
"

OPTERR=0

verbose=''
current_dir=''
backup_dir=''
test_target=''

while getopts vhb:c:t: opt
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
        c)
            current_dir=$OPTARG
            ;;
        t)
            test_target=$OPTARG
            ;;
        \?)
            echo "\n$(basename $0): Invalid option -$opt" >&2
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

backup_dir=$(echo "$backup_dir" | perl -pe 's/\/$//')

if [ -z "$current_dir" ]
then
    current_dir=$(pwd)
    test_target=""
fi

if [ "$verboseStubbed" = "-v" ]
then
    echo "current_dir=$current_dir"
    echo "backup_dir=$backup_dir"
    echo "test_target=$test_target"
fi

if [ "$backup_dir" = "$current_dir" ]
then
    echo "Cant use backup as current"
    exit 1
fi

function cleanLine {
    if [ "$verbose" = "-v" ] && [ ! -z "$COLUMNS" ]
    then
        echo -ne "\r"
        count=$COLUMNS
        while [ ! "$count" = "0" ]
        do
            echo -n " "
            count=$(($count-1))
        done
    fi
}

if [ "$test_target" = "" ]
then
    pushd "$backup_dir" >/dev/null
    options=
    find . ! -name '.' -exec $0 \
         $verbose \
         -b "$backup_dir" \
         -c "$current_dir" \
         -t "{}" \
    \; 2>/dev/null

    cleanLine
else
    test_target=$(echo "$test_target" | perl -pe 's|^./||')

    if [ "$verbose" = "-v" ]
    then
        echo -ne "?$backup_dir/$test_target\r"
    fi
    
    if [ -e "$backup_dir/$test_target" ] \
    && [ ! -e "$current_dir/$test_target" ]
    then
        cleanLine
        echo "-$test_target"
        rm -fr "$backup_dir/$test_target"
    fi

fi

