#!/usr/bin/python

# $Date: 2014-02-27 14:08:03 +1100 (Thu, 27 Feb 2014) $
# $Revision: 8921 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/validate.py $
# $Id: validate.py 8921 2014-02-27 03:08:03Z david.edson $

# inspired from the test suite file "xstc/xstc.py"
# thanks to Kasimier Buchcik
#

import sys, re, os, libxml2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('schema',action='store',help='schema name')
parser.add_argument('file',action='store',help='xml file')

args = parser.parse_args()

if args.verbose:
        nestPrint(vars(args),colour=True)

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
