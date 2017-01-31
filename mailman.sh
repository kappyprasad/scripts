#!/usr/bin/env bash

hostname='tpg.com.au'
username='eddo8888'
password=$(passwords.py -e "$hostname" -a "TPG" -u "$username")
email='eddo888@tpg.com.au'

if [ -z "$1" ]
then
    echo "usage: $(basename $0) [sr]"
    exit
fi

if [ "$1" = "-s" ]
then
    mailman.py \
        -s \
        -j "Test Subject at $(dateStamp.sh)" \
        -b "Test Body" \
        -t "$email" \
        -f _test/DavidEdson-hand.jpeg \
        -u "$username" \
        -p "$password"
fi

if [ "$1" = "-r" ]
then
    mailman.py \
        -rm \
        -u "$username" \
        -p "$password"

fi
