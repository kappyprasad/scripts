#!/usr/bin/env bash

file="$1"
name=$(echo $file | perl -pe 's/.gpg$//')
gpg -d -o "$name" "$file"
