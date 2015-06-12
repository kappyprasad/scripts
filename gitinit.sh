#!/usr/bin/env sh

existing=0
base="/Users/davidedson/Repository"
user=$(whoami)
host=localhost

usage="\
usage: $0 \n\
    -h         help\n\
    -e         use existing repo as source\n\
    -b base    git base dir\n\
"

while getopts heb: opt
do
    case $opt in
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
git init --bare
popd >/dev/null

function pushit {
    git remote add origin "$user@$host:$base/$repo.git"
    git push origin master
    git branch --set-upstream-to=origin/master master
    gitpush.sh
}

if [ $existing == 1 ] && [ -e "$repo/.git" ] 
then
    pushd "$repo"
    pushit
    popd
else
    pushd "$TEMP"
    mkdir -p "$repo"
    cd "$repo"
    git init
    echo target >> .gitignore
    echo "# $repo" > README.md
    gitadd.sh -a
    gitcommit.sh -m 'moved remote'
    pushit
    popd
fi

