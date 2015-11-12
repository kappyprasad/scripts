#!/usr/bin/env sh

envs=(Darwin Linux CYGWIN_NT-6.2-WOW64)

help="\
usage: $(basename $0) <repo>\n\
\n\
-v       Verbose\n\
-h       Help\n\
-E envn  in (${envs[@]})\n\
-H host  Hostname\n\
-P port  Portnum\n\
"

OPTERR=0

host=$(hostname)
port=8080
user=$(whoami)
envn=$(uname)

while getopts vhE:H:P: opt
do
    case $opt in
        v) 
            echo "verbose is on"
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        E)
            envn=$OPTARG
            ;;
        H) 
            host=$OPTARG
            echo "host=$host"
            ;;
        P) 
            port=$OPTARG
            echo "port=$port"
            ;;
        \?)
            echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

#spaces force word match, @ forces list iteration to check
if ! [[ " ${envs[@]} " =~ " ${envn} " ]]
then
    echo "$help"
    echo "env not in (${envs[@]})"
    exit 1
fi

horizontal.pl

echo "host=$host"
echo "port=$port"
echo "user=user"
echo "envn=$envn"


