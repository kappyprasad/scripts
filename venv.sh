#!/usr/bin/env bash

dir="$1"
if [ -z "$dir" ]
then
    echo "usage: $0 <dir>"
    exit 1
fi

mkdir "$dir"
cd "$dir"
virtualenv venv
source venv/bin/activate
which python
python --version


