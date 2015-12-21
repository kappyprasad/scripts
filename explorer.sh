#!/usr/bin/env bash

target="$*"
dospath=$(cygpath -d "$target")
echo "$dospath"
explorer.exe "$dospath"
