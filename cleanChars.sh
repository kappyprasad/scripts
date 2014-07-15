#!/bin/bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



perl -pe "s/[\x7F-\xFF]//g" -i "$*" 

