#!/bin/bash

envr=github.com
user=eddo888@tpg.com.au
pass=$(passwords.py -e $envr -u $user)

ppwd=$(basename $(dirname $(pwd)))
ownr=$(basename $(pwd))

echo $ppwd/$ownr

if [ "$ppwd" != "github.com" ]
then
    echo "parent pwd is not github.com" >&2
    exit 1
fi

gitrepos.py -u $user -p $pass -o $ownr $*
