#!/bin/bash

target="$*"
unixpath=$(cygpath -au "$target" | perl -pe 's|^/cygdrive/([a-z])|file://\1:|')
echo "$unixpath"
