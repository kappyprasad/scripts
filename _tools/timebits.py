#!/bin/bash

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import re

monthNames = {
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'Apr' : 4,
    'May' : 5,
    'Jun' : 6,
    'Jul' : 7,
    'Aug' : 8,
    'Sep' : 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12
}

dsp = '%Y-%m-%d'
tsp = '%H:%M:%S'

dtspattern = re.compile(
    '(\d{4})-(\d{2})-(\d{2})\s' +\
    '(\d{2}):(\d{2}):(\d{2})' +\
    '\.(\d+)'
)
