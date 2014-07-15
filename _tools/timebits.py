#!/bin/bash

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/timebits.py $
# $Id: timebits.py 11546 2014-06-04 06:05:55Z david.edson $

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
