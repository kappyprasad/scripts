#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v         Verbose\n\
-h         Help\n\
-c         clean deleted files\n\
-b backup  directory
-t         make target dir\n\
"

OPTERR=0

verbose=''
mkdtarget=''
backup_dir=''
clean=''

while getopts vhctb: opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        c)
            clean='-c'
            ;;
        b)
            backup_dir=$OPTARG
            ;;
        t)
            mkdtarget='-t'
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

current_dir=$(pwd)

if [ "$verbose" = "-v" ]
then
    echo $current_dir
    echo $backup_dir
fi

if [ "$backup_dir" = "$current_dir" ]
then
    echo "Cant backup to the same target"
    exit 1
fi

if [ "$mkdtarget" = "-t" ]
then
    mkdir -p $backup_dir
fi

if [ ! -d "$backup_dir" ]
then
    echo "the target $backup_dir doesn't exist"
    exit 1
fi

horizontal.pl

rsync --perms --times --partial --update -vr . $backup_dir | rsync.pl

if [ "$clean" = "-c" ]
then
    horizontal.pl
    notNeeded.sh -vb $backup_dir
fi
