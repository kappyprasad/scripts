#!/usr/bin/env bash

help="\
usage: $(basename $0)\n\
\n\
-v           Verbose   show detailed debug\n\
-h           Help      show this help message and exit\n\
-q           Query     structure no action\n\
-t           Test      only show commands don't execute\n\
-d display   =1        which display to use as the resolution\n\
-o offset    =0        place this number of screens to the right\n\
-r rows      =1        number of rows of terminals\n\
-c cols      =1        number of columns of terminals\n\
-f font      =6x14     font size used to calculate width/height\n\
-b base      =''       ssh -i epm user@host <execute>\n\
-e execute   =bash     execute this command on this terminal\n\
-E executes            execute this commands found on stdin\n\
"

# preset error for param validation
OPTERR=0

# presets for variables
verbose=''
query=''
test=''
display=1
offset=0
rows=1
cols=1
font='6x14'
base=''
execute='bash'
executes=''

# iterate through getopts on options
while getopts vhqto:d:r:c:f:b:e:E opt
do
    case $opt in
        v)  verbose='-v';;
        h)  echo -e "$help"; exit 0;;
        q)  query='-q';;
        t)  test='-t';;
        d)  display=$OPTARG;;
        o)  offset=$OPTARG;;
        r)  rows=$OPTARG;;
        c)  cols=$OPTARG;;
        f)  font=$OPTARG;;
        b)  base=$OPTARG;;
        e)  execute=$OPTARG;;
        E)  executes='-E';;
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

#horizontal.pl

declare -a commands

IFS=""
commands=()
if [ "$executes" = "-E" ]
then
    while read command
    do
        #echo "$command"
        commands+=($(echo $command | perl -pe 's/"/\\"/g;'))
    done
fi

while (( ${#commands[@]} < ( $rows * $cols) ))
do
    commands+=($execute)
done

if [ "$verbose" = "-v" ]
then
    for (( i = 0; i< ${#commands[@]}; i++ ))
    do
        echo "${commands[$i]}"
    done
fi

row=$rows
while (( $row > 0 )) 
do
    downset=$(( (($row - 1) * $down) - $fontheight ))
    
    col=$cols
    while (( $col > 0 ))
    do
        inset=$(( (($col - 1) * $over) + ($offset * $pixelwidth) ))

        command=${commands[0]}
        unset commands[0]
        commands=(${commands[@]})
                  
        if [ "$verbose" = "-v" ] || [  "$test" = "-t" ]
        then
            echo xterm -geometry ${width}x${height}+${inset}+${downset} -T "$command" -e "$base $command"
        fi
        
        if [ -z "$test" ]
        then
            xterm -geometry ${width}x${height}+${inset}+${downset} -T "$command" -e "$base $command" &
        fi
        
        col=$(( $col - 1 ))
    done

    row=$(( $row - 1 ))
done

