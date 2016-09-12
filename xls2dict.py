#!/usr/bin/env python

import sys,os,re,argparse,json,StringIO,xml,xmltodict,collections

from xlrd import open_workbook
from xlwt import Workbook

def argue():
    parser = argparse.ArgumentParser('Excel processor input/output by suffix')

    suffix=map(lambda x:'*.%s'%x, ['xls', 'xlsx', 'json', 'xml'])
    
    parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
    parser.add_argument('-c','--cdata',   action='store_true', help='force cdata')
    parser.add_argument('-f','--formula', action='store_true', help='use formulas')
    parser.add_argument('-i','--input',   action='store',      help='input file', required=True, metavar=','.join(suffix))
    parser.add_argument('-o','--output',  action='store',      help='output file', required=True, metavar=','.join(suffix))

    args = parser.parse_args()

    if args.verbose:
        sys.stderr.write('args:')
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')

    return args

def escape_hacked(data, entities={}):
    #print entities
    if any(x in data for x in ['<', '>', '&']):
        return '<![CDATA[%s]]>' % data
    return escape_orig(data, entities)

def xls2dict(input, verbose=False, formulas=False):
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
                v = s.cell(r,c).value 
                if formulas:
                    v = s.cell(r,c).value
                col = {
                    '@number' : '%d'%c,
                    '#text' : '%s'%v
                }
                row['col'].append(col)

    return js

def dict2xls(js, verbose=False, formulas=False):
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

    if args.cdata:
        escape_orig = xml.sax.saxutils.escape
        xml.sax.saxutils.escape = escape_hacked

    input = open(args.input,'rb')
        
    if args.input.lower().endswith('.xls') or args.input.lower().endswith('.xlsx'):
        js = xls2dict(input, verbose=args.verbose, formulas=args.formula)

    if args.input.lower().endswith('.json'):
        js = json.load(input)

    if args.input.lower().endswith('.xml'):
        js = xmltodict.parse(input,force_cdata=True)

    input.close()
    
    output = open(args.output,'w')

    if args.output.lower().endswith('.xls') or args.output.lower().endswith('.xlsx'):
        wb =dict2xls(js, verbose=args.verbose, formulas=args.formula)
        wb.save(args.output)

    if args.output.lower().endswith('.json'):
        json.dump(js,output,indent=4)

    if args.output.lower().endswith('.xml'):
        xmltodict.unparse(js,output=output,indent='    ',pretty=True)

    output.close()
        
    return


if __name__ == '__main__': main()

