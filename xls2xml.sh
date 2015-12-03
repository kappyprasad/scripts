#!/usr/bin/env bash

xslt=$(dirname $0)/xls2xml.xsl

xls="$1"

if [ ! -e "$xls" ]
then
    echo "usage: $(basename $0) <file.xls.xml>"
    exit
fi

xml=$(echo $xls | perl -pe 's/.xls.xml$/.xml/')

xsltproc -o "$xml" $xslt "$xls"

