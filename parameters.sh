#!/usr/bin/env sh

horizontal.pl
while getopts vhH:P: opt
do
    case $opt in
        v) 
            echo "verbose is on"
            ;;
        h) 
            echo "help is on"
            ;;
        H) 
            host=$OPTARG
            echo "host=$host"
            ;;
        P) 
            port=$OPTARG
            echo "port=$port"
            ;;
    esac
done

shift $((OPTIND-1))
horizontal.pl
for file in $*
do
    echo $file
done

