#!/usr/bin/env bash

save=~/tmp/$$

mkdir $save

for i in .classpath .project .settings
do
    mv -v $i $save/
    git rm -r $i
    git commit -m 'removed'
    echo .gitignore | grep -v $i > .gi; mv .gi .gitignore
    echo $i >> .gitignore
    git add .gitignore
    mv $save/$i .
    git commit -m 'ignored'
done

ls -la $save/

