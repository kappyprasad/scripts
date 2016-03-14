#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v       Verbose\n\
-h       Help\n\
-d disp  display=1\n\
-r rows  default=1\n\
-c cols  default=1\n\
-f font  default=6x14\n\
"

# preset error for param validation
OPTERR=0

# presets for variables
verbose=''
disp=1
rows=1
cols=1
font='6x14'

# iterate through getopts on options
while getopts vhd:r:c:f: opt
do
    case $opt in
        v)  verbose='-v';;
        h)  echo -e "$help"; exit 0;;
        d)  disp=$OPTARG;;
        r)  rows=$OPTARG;;
        c)  cols=$OPTARG;;
        f)  font=$OPTARG;;
        \?) echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2;exit 1;;
    esac
done

shift $((OPTIND-1))

reso=$(system_profiler SPDisplaysDataType | grep Resolution | head -$disp | tail -1)

fontwidth=$(echo $font | cut -d x -f 1)
fontheight=$(echo $font | cut -d x -f 2)

pixelwidth=$(echo $reso | perl -ne 'print "$1\n" if (/^\s*Resolution:\s+(\d+)\s+x\s+(\d+)\s.*/);')
pixelheight=$(echo $reso | perl -ne 'print "$2\n" if (/^\s*Resolution:\s+(\d+)\s+x\s+(\d+)\s.*/);')

over=$(($pixelwidth / $cols))
down=$(($pixelheight / $rows))

textwidth=$((($pixelwidth / $fontwidth) - 1))
textheight=$((($pixelheight / $fontheight) - 1))

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
    downset=$(((($row-1) * $down) - $fontheight))
    
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

