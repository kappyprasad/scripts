#!/usr/bin/env bash

file="$1"
gpg -er eddo888@tpg.com.au -o "$file.gpg" "$file"
