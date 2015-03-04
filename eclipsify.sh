#!/bin/bash

source=$(dirname $(which eclipsify.sh ))

repos="$*"

if [ -z "$repos" ]
then
    if [ -d .git ]
    then
	repos=$(pwd)
    else
    repos=*
    fi
fi

if [ ! -d "$source" ]
then
    echo 'cant find the $source directory'
    exit 1
fi

for i in $repos
do 
    if [ -d $i ]
    then
        if [ ! -f $i/.project ] 
        then 
            echo $i
            cp $source/.pydevproject $i/
            cp $source/.project $i/
            name=$(basename $i)
            xset.py -x '/projectDescription/name' -t $name $i/.project
            xset.py -x '/projectDescription/comment' -t $name $i/.project
        fi
    fi
done
