#!/usr/bin/env sh

base="/cygdrive/d/GIT"
repo="$1"

if [ -z "$repo" ] 
then
    echo "usage: $0 <repo>"
    exit 1
fi

if [ -e "$base/$repo.git" ]
then
    echo "$base/$repo.git already exists"
    exit 1
fi

cd "$base"
mkdir "$repo.git"
cd "$repo.git"
git init --bare

cd "$TEMP"
mkdir "$repo"
cd "$repo"
git init
echo "# $repo" > README.md
git add README.md
git commit -m 'repo created'
git remote add origin "$base/$repo.git"
git push origin master

