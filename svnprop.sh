#!/usr/bin/env sh

verbose=0
type="text/xml"

usage="\
usage: $(basename $0) -[vht] <files>\n\
    -v         verbose\n\
    -h         help\n\
    -t type    mime type, defaults to text/xml\n\
"

while getopts vht: opt
do
    case $opt in
        v) 
            verbose=1
            ;;
        h)
            echo -e "$usage"
            exit 
            ;;
        t) 
            type=$OPTARG
            ;;
    esac
done

if [ $verbose == 1 ]
then
    echo 1>&2
    echo "verbose=$verbose" 1>&2
    echo "type=$type" 1>&2
    echo 1>&2
fi

shift $((OPTIND-1))

if [ $# != 1 ]
then
    echo -e "$usage"
    exit
fi

echo svn propset svn:mime-type "$type" $*
