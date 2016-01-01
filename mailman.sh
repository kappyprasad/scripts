#!/usr/bin/env bash

if [ -z "$1" ]
then
    echo "usage: $(basename $0) [sr]"
    exit
fi

if [ "$1" = "-s" ]
then
    mailman.py \
        -s \
        -j "Test Subject" \
        -b "Test Body" \
        -t eddo888@tpg.com.au \
        -f _test/DavidEdson-hand.jpeg
fi

if [ "$1" = "-r" ]
then
    mailman.py \
        -r 

fi
