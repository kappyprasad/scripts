#!/usr/bin/env bash

for i in "$*"
do
    j=$(basename "$i")
    mkshortcut "$i" -n "$j"
    ls "$j.lnk"
done
