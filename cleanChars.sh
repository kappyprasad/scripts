#!/bin/bash

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/cleanChars.sh $
# $Id: cleanChars.sh 7279 2013-12-12 14:22:40Z david.edson $

perl -pe "s/[\x7F-\xFF]//g" -i "$*" 

