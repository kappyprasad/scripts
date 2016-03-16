#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v           Verbose   show detailed debug\n\
-h           Help      show this help message and exit\n\
-q           Query     structure no action\n\
-d display   =1        which display to use as the resolution\n\
-o offset    =0        place this number of screens to the right\n\
-r rows      =1        number of rows of terminals\n\
-c cols      =1        number of columns of terminals\n\
-f font      =6x14     font size used to calculate width/height\n\
-e execute   =bash     execute this command on this terminal\n\
"

# preset error for param validation
OPTERR=0

# presets for variables
verbose=''
query=''
display=1
offset=0
rows=1
cols=1
font='6x14'
execute='bash'

# iterate through getopts on options
while getopts vhqo:d:r:c:f:e: opt
do
    case $opt in
        v)  verbose='-v';;
        h)  echo -e "$help"; exit 0;;
        q)  query='-q';;
        d)  display=$OPTARG;;
        o)  offset=$OPTARG;;
        r)  rows=$OPTARG;;
        c)  cols=$OPTARG;;
        f)  font=$OPTARG;;
        e)  execute=$OPTARG;;
        \?) echo "\n$(basename $0): Invalid option -$opt\n\n$help\n" >&2;exit 1;;
    esac
done

shift $((OPTIND-1))

reso=$(system_profiler SPDisplaysDataType | grep Resolution | head -$display | tail -1)

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

if [ "$query" = "-q" ] || [ "$verbose" = "-v" ]
then
    echo "display=$display"
    echo "offset=$offset"
    echo "rows/cols=$rows/$cols"
    echo "width/height=$pixelwidth/$pixelheight"
    echo "chars/lines=$textwidth/$textheight"

    if [ "$query" = "-q" ]
    then
        exit
    fi
fi

horizontal.pl

row=$rows
while [ "$row" != "0" ] 
do
    downset=$(( (($row - 1) * $down) - $fontheight ))
    
    col=$cols
    while [ "$col" != "0" ]
    do
        inset=$(( (($col - 1) * $over) + ($offset * $pixelwidth) ))

        if [ "$verbose" = "-v" ]
        then
            echo xterm -geometry ${width}x${height}+${inset}+${downset} -T "$execute" -e "$execute"
        fi
        xterm -geometry ${width}x${height}+${inset}+${downset} -T "$execute" -e "$execute" &

        col=$(( $col - 1 ))
    done

    row=$(( $row - 1 ))
done

