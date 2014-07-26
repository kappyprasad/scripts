#!/usr/bin/bash

# $Date: 2014-06-19 08:22:37 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4727 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/bin/cleanBackupFiles.sh $
# $Id: cleanBackupFiles.sh 4727 2014-06-18 22:22:37Z dedson $



find . \( -name "error.log" -or -iname "thumbs.db" -or -iname "\#*" -or -iname "~*" -or -iname "*~" -or -iname "nohup.out" -or -iname "*.bak" -or -iname "*.stackdump" \) -exec rm -vf {} \;


