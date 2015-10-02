#!/usr/bin/env sh

help="\
usage: $(basename $0) <repo>\n\
\n\
-v       Verbose\n\
-h       Help\n\
-H host  Hostname\n\
-P port  Portnum\n\
"

OPTERR=0

while getopts vhH:P: opt
do
    case $opt in
        v) 
            echo "verbose is on"
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        H) 
            host=$OPTARG
            echo "host=$host"
            ;;
        P) 
            port=$OPTARG
            echo "port=$port"
            ;;
        \?)
            echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

horizontal.pl
for file in $*
do
    echo $file
done

