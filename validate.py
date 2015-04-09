#!/usr/bin/python

import sys, re, os, libxml2, argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-s','--schema',  action='store', help='schema name')
parser.add_argument('xml',            action='store', help='xml file')

args = parser.parse_args()

if args.verbose:
        prettyPrint(vars(args),colour=True)

doc = libxml2.parseFile(args.xml)

if args.schema:
    schema = args.schema
else:
    spath = doc.getRootElement().prop('schemaLocation').split(' ')[1]
    dpath = os.path.dirname(args.xml)
    schema = '%s/%s'%(dpath,spath)

sys.stderr.write('schema=%s\n'%schema)

ctxt = libxml2.schemaNewParserCtxt(schema)
schema = ctxt.schemaParse()
del ctxt

validationCtxt = schema.schemaNewValidCtxt()


#instance_Err = validationCtxt.schemaValidateFile(filePath, 0)
instance_Err = validationCtxt.schemaValidateDoc(doc)

del validationCtxt
del schema
doc.freeDoc()

if instance_Err != 0:
        print "VALIDATION FAILED"
else:
    print "VALIDATED"
