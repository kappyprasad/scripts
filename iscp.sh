#!/bin/bash

rsync --perms --times --executability --partial --rsh=issh.sh $*
 
