#!/usr/bin/env sh

verbose=0
existing=0
base="/cygdrive/d/GIT"

usage="\
usage: $0 \n\
    -v         verbose\n\
    -h         help\n\
    -e         use existing repo as source\n\
    -b base    git base dir\n\
"

while getopts vheb: opt
do
    case $opt in
        v) 
            verbose=1
            echo "verbose is on" 1>&2
            ;;
        h)
            echo -e "$usage"
            exit 
            ;;
        e) 
            existing=1
            echo "upload existing" 1>&2
            ;;
        b) 
            base=$OPTARG
            echo "base=$base" 1>&2
            ;;
    esac
done

shift $((OPTIND-1))

repo="$1"

if [ -z "$repo" ] 
then
    echo "usage: $0 <repo>"
    exit 1
fi

if [ "$repo" == "." ]
then
    repo=$(basename $(pwd))
fi

repo=$(echo $repo | perl -pe 's|/$||')

if [ -e "$base/$repo.git" ]
then
    echo "$base/$repo.git already exists"
    exit 1
fi

pushd "$base" >/dev/null
mkdir -p "$repo.git"
cd "$repo.git"
if [ $verbose == 1 ]
then 
    echo "cd $(pwd)"
    echo git init --bare
fi
git init --bare
popd >/dev/null

if [ $existing == 1 ] && [ -e "$repo/.git" ] 
then
    cd "$repo"
    cleanBackupFiles.sh
    if [ $verbose == 1 ]
    then 
        echo "cd $(pwd)"
        echo gitadd.sh -a
    fi
    gitadd.sh -a
    
else
    cd "$TEMP"
    mkdir -p "$repo"
    cd "$repo"
    if [ $verbose == 1 ]
    then
        echo "cd $(pwd)"
        echo git init
        echo "# $repo" > README.md
        echo git add README.md
    fi
    git init
    echo "# $repo" > README.md
    git add README.md
fi

if [ $verbose == 1 ]
then
    echo git commit -m 'repo created'
    echo git remote add origin "$base/$repo.git"
    echo git push origin master
fi

git commit -m 'repo created'
git remote add origin "$base/$repo.git"
git push origin master

