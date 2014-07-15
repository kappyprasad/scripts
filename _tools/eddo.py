#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/eddo.py $
# $Id: eddo.py 11546 2014-06-04 06:05:55Z david.edson $

import sys,os
from _tools.colours import colours

replacements = {
  '\n' : '\\n',
  '\\"'  : '&quot;',
  '"'  : '\\"',
  '&quot;' : '\\"'
}

def getColumns():
  if 'COLUMNS' in os.environ:
    return int(os.environ['COLUMNS'])
  return 80
  
def buildHorizon(char='-'):
  return getColumns() * char

def fixString(dirty):
  clean = dirty
  for replacement in replacements.keys():
    clean = clean.replace(replacement,replacements[replacement])
  return clean

