#!/bin/bash

perl -pe "s/[\x7F-\xFF]//g" -i "$*" 

