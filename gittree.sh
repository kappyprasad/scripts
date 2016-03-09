#!/usr/bin/env bash

originList=$(git remote)
echo "originList="
for origin in ${originList[@]}
do
    echo -e "\t$origin"
done

origin=$(git branch -vv | perl -ne 'print "$1\n" if (/^\*\s+\S+\s+\S+\s\[([^\]]*)\].*/);') 
echo "origin=$origin"

branchList=$(git branch | cut -c 3-)
echo "branchList="
for branch in ${branchList[@]}
do
    echo -e "\t$branch"
done

branch=$(git branch -vv | perl -ne 'print "$1\n" if (/^\*\s+(\S+)\s+/);')
echo "branch=$branch"



