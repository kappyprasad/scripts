#!/usr/bin/env bash

rsync --perms --times --executability --partial --rsh=ssh.sh "$*"
 
