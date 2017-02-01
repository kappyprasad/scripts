#!/usr/bin/env bash

hostname='tpg.com.au'
username='eddo8888'
password=$(passwords.py -e "$hostname" -a "TPG" -u "$username")
email='eddo888@tpg.com.au'

if [ -z "$1" ]
then
    echo "usage: $(basename $0) [srmd]"
    exit
fi

if [ "$1" = "-s" ]
then
    mailman.py \
        -u "$username" \
        -p "$password" \
        send \
        "$email" \
        "$email" \
        "Test Subject at $(dateStamp.sh)" \
        "Test Body" \
        _test/DavidEdson-hand.jpeg
fi

if [ "$1" = "-r" ]
then
    mailman.py \
        -u "$username" \
        -p "$password" \
        read

fi

