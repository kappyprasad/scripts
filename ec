#!/bin/bash
 
params=()
for p in "$@"; do
    if [ "$p" == "-n" ]; then
        params+=( "$p" )
    elif [ "${p:0:1}" == "+" ]; then
        params+=( "$p" )
    else
        params+=( "/ssh:ec2:"$(readlink -f $p) )
    fi
done
emacsclient "${params[@]}"
