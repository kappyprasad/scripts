#!/usr/bin/python

import sys,os,re,argparse,json,StringIO,xmltodict
from xlrd import open_workbook
from xlwt import Workbook

parser = argparse.ArgumentParser('Excel processor input/output in xls,json,xml')

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-o','--output',  action='store',      help='output file')

groupI = parser.add_mutually_exclusive_group(required=True)
groupI.add_argument('-l', '--iXLS',   action='store', help='input is excel')
groupI.add_argument('-j', '--iJSON',  action='store', help='input is json')
groupI.add_argument('-x', '--iXML',   action='store', help='input is xml')

groupO = parser.add_mutually_exclusive_group(required=True)
groupO.add_argument('-L', '--oXLS',   action='store_true', help='output is excel')
groupO.add_argument('-J', '--oJSON',  action='store_true', help='output is json')
groupO.add_argument('-X', '--oXML',   action='store_true', help='output is xml', )

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args:')
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

def xls2dict(input):
    js = {
        'workbook' : {
            'sheet' : []
        }
    }

    wb = open_workbook(file_contents=input.read())
    if args.verbose:
        sys.stderr.write('%s\n'%wb)

    for s in wb.sheets():
        if args.verbose:
            sys.stderr.write('%s\n'%s)

        sheet = {
            '@name' : '%s'%s.name,
            'row': []
        }
        js['workbook']['sheet'].append(sheet)

        for r in range(s.nrows):
            if args.verbose:
                sys.stderr.write('\trow=%0d\n'%r)
            row = {
                '@number' : '%d'%r,
                'col' : []
            }
            sheet['row'].append(row)

            for c in range(s.ncols):
                if args.verbose:
                    sys.stderr.write('\t\tcol=%0d = %s\n'%(c,s.cell(r,c)))
                col = {
                    '@number' : '%d'%c,
                    '#text' : '%s'%s.cell(r,c).value
                }
                row['col'].append(col)

    return js

def dict2xls(js):
    if args.verbose:
        json.dump(js,sys.stderr,indent=4)
        sys.stderr.write('\n')

    wb = Workbook()
    if args.verbose:
        sys.stderr.write('%s\n'%wb)

    w = js['workbook']
    sheets = w['sheet']
    if type(sheets) is not list:
        sheets = [ sheets ]

    for s in sheets:
        sheet = wb.add_sheet(s['@name'])
        if args.verbose:
            sys.stderr.write('%s\n'%sheet)

        rows = s['row']
        if type(rows) is not list:
            rows = [ rows ]

        for r in rows:
            row = int(r['@number'])
            if args.verbose:
                sys.stderr.write('\trow=%0d\n'%row)

            cols = r['col']
            if type(cols) is not list:
                cols = [ cols ]

            for c in cols:
                col = int(c['@number'])
                text = c['#text']
                if args.verbose:
                    sys.stderr.write('\t\tcol=%0d = %s\n'%(col,text))
                
                sheet.write(row,col,text)

    return wb

def main():
    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout
    
    if args.iXLS:
        input = open(args.iXLS,'rb')
        js = xls2dict(input)
        input.close()

    if args.iJSON:
        input = open(args.iJSON)
        js = json.load(input)
        input.close()
        None

    if args.iXML:
        input = open(args.iXML)
        js = xmltodict.parse(input)
        input.close()
        None

    if args.oXLS:
        if args.output:
            wb =dict2xls(js)
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

