#!/usr/bin/env bash

rsync --perms --times --executability --partial --rsh=issh.sh $*
 
