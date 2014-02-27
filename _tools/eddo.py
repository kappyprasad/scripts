#!/usr/bin/python

import sys,os
from _tools.colours import colours

replacements = {
  '\n' : '\\n',
  '\\"'  : '&quot;',
  '"'  : '\\"',
  '&quot;' : '\\"'
}

def buildHorizon():
  if 'COLUMNS' in os.environ:
    horizon = '-' * int(os.environ['COLUMNS'])
  else:
    horizon = '-' * 80
  return horizon

def fixString(dirty):
  clean = dirty
  for replacement in replacements.keys():
    clean = clean.replace(replacement,replacements[replacement])
  return clean

def nestPrint(d, indent='', colour=False, output=sys.stdout):
  if not colour:
    for key in colours.keys():
      colours[key] = ''
  t='%s'%type(d)
  if d is None:
    output.write('%sNone%s'%(colours['Off'],colours['Off']))
  elif t == 'org.python.core.PyDictionary' or t == '<type \'dict\'>':
    output.write('%s{%s\n'%(colours['Purple'],colours['Off']))
    keys = d.keys()
    for i in range(len(keys)):
      key = keys[i]
      output.write(
        '%s  "%s%s%s" :  ' % (
          indent,colours['Red'],
          key,colours['Off']
          )
        )
      nestPrint(d[key], indent='%s  ' % indent, colour=colour, output=output)
      if i < (len(keys) - 1):
        output.write(',\n')
      else:
        output.write('\n')
    output.write('%s%s}%s' %(indent,colours['Purple'],colours['Off']))
  elif t == 'org.python.core.PyList' or t == '<type \'list\'>':
    bracketPrint(
      d, 
      '%s[%s'%(colours['Teal'],colours['Off']), 
      '%s]%s'%(colours['Teal'],colours['Off']), 
      '  %s'%indent, 
      colour,
      output
    )
  elif t == 'org.python.core.PyTuple' or t == '<type \'tuple\'>':
    bracketPrint(
      d, 
      '%s(%s'%(colours['Purple'],colours['Off']), 
      '%s)%s'%(colours['Purple'],colours['Off']), 
      '  %s'%indent, 
      colour,
      output
    )
  elif t == 'org.python.core.PyString' or t == '<type \'str\'>':
    output.write('"%s%s%s"' %(colours['Green'],fixString(d),colours['Off']))
  else:
    output.write('%s%s%s' % (colours['Green'],d,colours['Off']))
    #print type(d), d
  if len(indent) == 0:
    output.write('\n')
  return

def bracketPrint(d, start, end, indent, colour=False, output=sys.stdout):
  
  output.write('%s\n' % start)
  for i in range(len(d)):
    output.write('%s' % (indent))
    nestPrint(d[i], indent='%s' % indent, colour=colour, output=output)
    if i < (len(d) - 1):
      output.write(',\n')
    else:
      output.write('\n')
  output.write('%s%s' % (indent[:-2], end))
  return

