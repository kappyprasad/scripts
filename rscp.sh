#!/bin/bash

rsync --perms --times --executability --partial --rsh=ssh.sh $*
 
