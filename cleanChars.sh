#!/usr/bin/env bash

replace="s/[\x7F-\xFF]//g;"

if [ -z "$1" ]
then
    perl -pe "$replace"
else
    perl -pe "$replace" -i "$*" 
fi
