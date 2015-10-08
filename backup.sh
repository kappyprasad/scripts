#!/bin/bash

# $Date: 2014-06-19 08:22:37 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4727 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/bin/backup.sh $
# $Id: backup.sh 4727 2014-06-18 22:22:37Z dedson $



drive=$1

if [ "$drive" = "" ]
then
    echo "usage: "`basename $0`" <drive:>"
    exit 1
fi

drive=`echo $drive | sed -e "s/://"`

current_dir=`pwd`
current_drive=`pwd | perl -ne 'print"$1\n" if (/^\/cygdrive\/(.)\//);'`

backup_dir=`pwd | perl -pe "s|/cygdrive/$current_drive/|/cygdrive/$drive/|"`

#echo $current_dir
#echo $backup_dir

if [ "$backup_dir" = "$current_dir" ]
then
    echo "Cant backup to the same drive"
    exit 1
fi

if [ ! -d "/cygdrive/$drive" ]
then
    echo "the drive /cygdrive/$drive doesn't exist"
    exit 1
fi

echo "------------------------------------------------------------------------------------------------------" >>error.log
date >>error.log


horizontal.pl

if [ ! -d $backup_dir ]
then
    echo "no path found $backup_dir"
    exit 1
fi

#exit

find . -maxdepth 1 ! -name . -exec cp -rvfup {} $backup_dir 2>>error.log \; | perl -ne '$|=1; print "+ $1\n" if (/^.(.*). ->/);'

horizontal.pl

pushd $backup_dir > /dev/null

if pwd | grep $backup_dir > /dev/null
then
    notNeeded.pl $current_dir 2>>error.log | perl -ne '$|=1;print "- $1\n" if (/^removed\s+`.\/(.*).$/);'
else
    echo "no path found $backup_dir"
fi

popd > /dev/null

horizontal.pl

