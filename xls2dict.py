#!/usr/bin/env python

import sys,os,re,argparse,json,StringIO,xml,xmltodict,collections

from xlrd import open_workbook
from xlwt import Workbook

def argue():
    parser = argparse.ArgumentParser('Excel processor input/output in xls,json,xml')

    parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
    parser.add_argument('-i','--input',   action='store',      help='input file')
    parser.add_argument('-o','--output',  action='store',      help='output file')

    groupI = parser.add_mutually_exclusive_group(required=True)
    groupI.add_argument('-e', '--iXLS',   action='store_true', help='input is excel')
    groupI.add_argument('-j', '--iJSON',  action='store_true', help='input is json')
    groupI.add_argument('-x', '--iXML',   action='store_true', help='input is xml')

    groupO = parser.add_mutually_exclusive_group(required=True)
    groupO.add_argument('-E', '--oXLS',   action='store_true', help='output is excel')
    groupO.add_argument('-J', '--oJSON',  action='store_true', help='output is json')
    groupO.add_argument('-X', '--oXML',   action='store_true', help='output is xml', )

    args = parser.parse_args()

    if args.verbose:
        sys.stderr.write('args:')
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')

    return args

def escape_hacked(data, entities={}):
    if data[0] == '<' and  data.strip()[-1] == '>':
        return '<![CDATA[%s]]>' % data
    return escape_orig(data, entities)

def xls2dict(input,verbose=False):
    js = {
        'workbook' : {
            'sheet' : []
        }
    }

    wb = open_workbook(file_contents=input.read())
    if verbose:
        sys.stderr.write('%s\n'%wb)

    for s in wb.sheets():
        if verbose:
            sys.stderr.write('%s\n'%s)

        sheet = {
            '@name' : '%s'%s.name,
            'row': []
        }
        js['workbook']['sheet'].append(sheet)

        for r in range(s.nrows):
            if verbose:
                sys.stderr.write('\trow=%0d\n'%r)
            row = {
                '@number' : '%d'%r,
                'col' : []
            }
            sheet['row'].append(row)

            for c in range(s.ncols):
                if verbose:
                    sys.stderr.write('\t\tcol=%0d = %s\n'%(c,s.cell(r,c)))
                col = {
                    '@number' : '%d'%c,
                    '#text' : '%s'%s.cell(r,c).value
                }
                row['col'].append(col)

    return js

def dict2xls(js,verbose=False):
    if verbose:
        json.dump(js,sys.stderr,indent=4)
        sys.stderr.write('\n')

    wb = Workbook()
    if verbose:
        sys.stderr.write('%s\n'%wb)

    w = js['workbook']
    sheets = w['sheet']
    if type(sheets) is not list:
        sheets = [ sheets ]

    for s in sheets:
        sheet = wb.add_sheet(s['@name'])
        if verbose:
            sys.stderr.write('%s\n'%sheet)

        if 'row' not in s.keys():
            continue
        rows = s['row']
        if type(rows) is not list:
            rows = [ rows ]
        
        for row in range(len(rows)):
            r = rows[row]
            if '@number' in r.keys():
                row = int(r['@number'])
                
            if verbose:
                sys.stderr.write('\trow=%0d\n'%row)

            if 'col' not in r.keys():
                continue
            cols = r['col']
            if type(cols) is not list:
                cols = [ cols ]

            for col in range(len(cols)):
                c = cols[col]
                if type(c) in [ dict, collections.OrderedDict ]:
                    if '@number' in c.keys():
                        col = int(c['@number'])
                    if '#text' in c.keys():
                        text = c['#text']
                    else:
                        text = ''
                else:
                    text = c
                if verbose:
                    sys.stderr.write('\t\tcol=%0d = %s\n'%(col,text))

                sheet.write(row,col,text)

    return wb

def main():
    global args, escape_orig
    args=argue()

    escape_orig = xml.sax.saxutils.escape
    xml.sax.saxutils.escape = escape_hacked

    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout

    if args.input:
        input = open(args.input,'rb')
    else:
        input = sys.stdin
        
    if args.iXLS:
        js = xls2dict(input,verbose=args.verbose)

    if args.iJSON:
        js = json.load(input)

    if args.iXML:
        js = xmltodict.parse(input,force_cdata=True)

    if args.input:
        input.close()
    
    if args.oXLS:
        if args.output:
            wb =dict2xls(js,verbose=args.verbose)
            wb.save(args.output)
        else:
            sys.stderr.write('please specify -o output') 

    if args.oJSON:
        json.dump(js,output,indent=4)

    if args.oXML:
        xmltodict.unparse(js,output=output,indent='    ',pretty=True)

    if args.output:
        output.close()
        
    return


if __name__ == '__main__': main()

