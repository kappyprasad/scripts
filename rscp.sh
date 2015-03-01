#!/bin/bash

# $Date: 2014-06-19 08:22:37 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4727 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/bin/rscp.sh $
# $Id: rscp.sh 4727 2014-06-18 22:22:37Z dedson $



rsync --partial --progress --rsh=ssh $*
 
