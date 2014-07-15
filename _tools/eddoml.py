#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/eddoml.py $
# $Id: eddoml.py 11546 2014-06-04 06:05:55Z david.edson $

import sys,re,os
from _tools.eddo import *

p=re.compile('[^A-Za-z0-9_]+')

replaxements = {
  '&' : '&amp;',
  '<' : '&lt;',
  '>' : '&gt;'
}

def fixStringXML(dirty):
  clean = dirty
  for replacement in replaxements.keys():
    clean = clean.replace(replacement,replaxements[replacement])
  return clean


def nestPrintXML(d, indent='', output=sys.stdout):
  t='%s'%type(d)
  if t == 'org.python.core.PyDictionary' or t == '<type \'dict\'>':
    output.write('\n')
    keys = d.keys()
    for i in range(len(keys)):
      key = keys[i]
      element = key
      while p.match(element):
        element = p.sub('',element)
      output.write('%s  <%s>' % (indent,element))
      nestPrintXML(d[key], indent='%s  ' % indent, output=output)
      output.write('</%s>\n'%element)
    output.write('%s' %indent)
  elif t == 'org.python.core.PyList' or t == '<type \'list\'>':
    bracketPrintXML(d, '  %s'%indent, output)
  elif t == 'org.python.core.PyTuple' or t == '<type \'tuple\'>':
    bracketPrintXML(d, '  %s'%indent, output)
  elif t == 'org.python.core.PyString' or t == '<type \'str\'>':
    output.write('%s'%fixStringXML(d))
  else:
    output.write('%s'%d)
  if len(indent) == 0:
    output.write('\n')
  return

def bracketPrintXML(d, indent, output=sys.stdout):
  for i in range(len(d)):
    output.write('%s<item>' % (indent))
    nestPrintXML(d[i], indent='%s' % indent, output=output)
    output.write('%s</item>' % (indent))
  return

