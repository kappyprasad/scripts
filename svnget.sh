#!/usr/bin/env sh

verbose=0
help=0
test=0

base=""
envr=$(hostname)
user=$(whoami)


while getopts vhtB:E:U: opt
do
  case $opt in 
    v)
      echo "verbose is on"
      verbose=1
      ;;
    h)
      echo "help is on"
      help=1
      ;;
    t)
      echo "test only is on"
      test=1
      ;;
    B)
      base=$OPTARG
      echo "base=$base"
      ;;
    E)
      envr=$OPTARG
      echo "envr=$envr"
      ;;
    U)
      user=$OPTARG
      echo "user=$user"
      ;;
  esac
done

shift $((OPTIND-1))

pass=$(passwords.py -e $envr -a svn -u $user)

curl -u "$user:$pass" "$base/" \
| perl -ne 'print "$1\n" if (/<li><a href="([^"]*)"/);' \
> .repositories

if [ "$verbose" = "1" ]
then
    cat .repositories
fi

if [ "$test" = "1" ]
then
    echo "test run only, exiting"
    exit
fi

for url in $(cat .repositories)
do
  if [ ! -d "$url" ]
  then
      horizontal.pl
      echo "+$url"
      mkdir "$url"
      pushd "$url" > /dev/null
      horizontal.pl
      pwd
      svn checkout "$base/$url/trunk"
      popd > /dev/null
  else
      echo "=$url"
  fi
done





