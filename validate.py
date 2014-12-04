#!/usr/bin/python




# inspired from the test suite file "xstc/xstc.py"
# thanks to Kasimier Buchcik
#

import sys, re, os, libxml2
import argparse

from _tools.pretty import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('schema',action='store',help='schema name')
parser.add_argument('file',action='store',help='xml file')

args = parser.parse_args()

if args.verbose:
        prettyPrint(vars(args),colour=True)

ctxt = libxml2.schemaNewParserCtxt(args.schema)
schema = ctxt.schemaParse()
del ctxt

validationCtxt = schema.schemaNewValidCtxt()

doc = libxml2.parseFile(args.file)

#instance_Err = validationCtxt.schemaValidateFile(filePath, 0)
instance_Err = validationCtxt.schemaValidateDoc(doc)

del validationCtxt
del schema
doc.freeDoc()

if instance_Err != 0:
        print "VALIDATION FAILED"
else:
    print "VALIDATED"
