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

def dict2eval(dictionary):
    pattern = re.compile('^([0-9a-zA-Z]*)(\[[0-9]+\])$')
    expression = ''
    for exp in dictionary.split('.'):
        m = pattern.match(exp)
        if m:
            expression += '["%s"]%s'%m.groups()
        else:
            expression += '["%s"]'%exp
    return expression

def main():
    dictionary = 'projects.project.modelType.objectType[0][2]'
    print dictionary
    print dict2eval(dictionary)
    return

if __name__ == '__main__': main()
