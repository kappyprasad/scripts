#!/usr/bin/env bash

help="\
usage: $(basename $0) <repo>\n\
\n\
-v       Verbose\n\
-h       Help\n\
-d disp  display=1\n\
-r rows  default=1\n\
-c cols  default=1\n\
"

# preset error for param validation
OPTERR=0

# presets for variables
verbose=''
disp=1
rows=1
cols=1

# iterate through getopts on options
while getopts vhd:r:c: opt
do
    case $opt in
        v) 
            verbose='-v'
            ;;
        h) 
            echo "$help"
            exit 0
            ;;
        d)
            disp=$OPTARG
            ;;
        r)
            rows=$OPTARG
            ;;
        c) 
            cols=$OPTARG
            ;;
        \?)
            # everything else is invalid
            echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND-1))

# check item is in list variable
# spaces force word match, @ forces list iteration to check
if ! [[ " ${envs[@]} " =~ " ${envn} " ]]
then
    echo "$help"
    echo "env not in (${envs[@]})"
    exit 1
fi

reso=$(system_profiler SPDisplaysDataType | grep Resolution | head -$disp | tail -1)

pixelwidth=$(echo $reso | perl -ne 'print "$1\n" if (/^\s*Resolution:\s+(\d+)\s+x\s+(\d+)\s.*/);')
pixelheight=$(echo $reso | perl -ne 'print "$2\n" if (/^\s*Resolution:\s+(\d+)\s+x\s+(\d+)\s.*/);')

over=$(($pixelwidth / $cols))
down=$(($pixelheight / $rows))

textwidth=$((($pixelwidth / 6) - 1))
textheight=$((($pixelheight / 14) - 1))

width=$(($textwidth / $cols))
height=$(($textheight / $rows))

if [ "$verbose" = "-v" ]
then
    horizontal.pl
    echo "disp=$disp"
    echo "size=$rows/$cols"
    echo "pixxles=$pixelwidth/$pixelheight"
    echo "text=$textwidth/$textheight"
fi

horizontal.pl

row=$rows
while [ "$row" != "0" ] 
do
    downset=$(((($row-1) * $down) - 14))
    
    col=$cols
    while [ "$col" != "0" ]
    do
        inset=$((($col-1) * $over))

        if [ "$verbose" = "-v" ]
        then
            echo xterm -geometry ${width}x${height}+${inset}+${downset}
        fi
        xterm -geometry ${width}x${height}+${inset}+${downset} &

        col=$(($col - 1))
    done

    row=$(($row - 1))
done

