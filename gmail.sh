#!/usr/bin/env bash

mailman.py -e -S imap.gmail.com -N 993 -u david.edson@gmail.com -T IMAP $*

