#!/usr/bin/env sh

xslt="$EDDO_PATH/Outliner/xslt/xml2outliner.xsl"

for xml in $*
do
    echo $xml.opml
    xsltproc $xslt $xml > $xml.opml
    xset.py -x '/opml/head/title' -t "$xml" $xml.opml
done


