#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



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

