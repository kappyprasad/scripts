#!/bin/bash

if [ -d .git ]
then
    repos=$(pwd)
    source=../scripts
else
    repos=*
    source=scripts
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
            xset.py -x '/projectDescription/name' -t $i $i/.project
        fi
    fi
done
