#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/pyson.py $
# $Id: pyson.py 11546 2014-06-04 06:05:55Z david.edson $


import sys,os,re

from _tools.eddo import *

replacements = {
    ': false' : ':False',
    ': true'  : ':True',
    ': null'  : ':None',
    ':false' : ':False',
    ':true'  : ':True',
    ':null'  : ':None',
    '[null'  : '[None',
    ',null'  : ',None',
}

def cleanJSON(lines):
    clean = lines
    for replacement in replacements.keys():
        while replacement in clean:
            clean = clean.replace(replacement,replacements[replacement])
    return eval(clean)

