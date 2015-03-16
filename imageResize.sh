#!/usr/bin/env bash

dir=$(pwd)
find "$dir" -name "*@2x.png" | while read image; do

    outfile=$(dirname "$image")/$(basename "$image" @2x.png).png

    if [ "$image" -nt "$outfile" ]; then

	basename "$image"

        width=$(identify "$image" | perl -ne 'print "$1\n" if(/ PNG (\d+)x\d+ /);')
        height=$(identify "$image" | perl -ne 'print "$1\n" if(/ PNG \d+x(\d+) /);')

	width=$(echo "$width/2" | bc)
	height=$(echo "$height/2" | bc)

        convert "$image" -resize "${width}x${height}" "$outfile"

        test "$outfile" -nt "$image" || exit 1
    fi
done
