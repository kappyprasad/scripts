#!/bin/bash

if [ ! -d scripts ]
then
    echo 'you are not in the eddo888 directory'
    exit 1
fi

for i in *
do 
    if [ -d $i ]
    then 
        if [ ! -f $i/.project ] 
        then 
            echo $i
            cp scripts/.pydevproject $i/
            cp scripts/.project $i/
            xset.py -x '/projectDescription/name' -t $i $i/.project
        fi
    fi
done
