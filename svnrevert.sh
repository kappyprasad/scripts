#!/bin/bash

# $Date: 2014-03-03 16:38:15 +1100 (Mon, 03 Mar 2014) $
# $Revision: 8986 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/svnrevert.sh $
# $Id: svnrevert.sh 8986 2014-03-03 05:38:15Z david.edson $

echo=""

if [ "$1" = "-v" ]
then
    echo=echo
fi

svn status | perl -ne 'print "$1\n" if (/^[\!]\s+(\S.*)$/);' | xargs -r -I FILE -d '\n\r' $echo svn delete "FILE"
svn status | perl -ne 'print "$1\n" if (/^[ADM]\s+(\S.*)$/);' | xargs -r -I FILE -d '\n\r' $echo svn revert --depth infinity "FILE"
