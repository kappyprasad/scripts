#!/usr/bin/env python

import sys,os,re,argparse,json,datetime,StringIO,xml,xmltodict,collections,xlrd

from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook

def argue():
    parser = argparse.ArgumentParser('Excel processor input/output by suffix')

    suffix=map(lambda x:'*.%s'%x, ['xls', 'xlsx', 'json', 'xml', 'md'])
    
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

def dateFixer(workbook,value):
    dts = '%Y-%m-%d %H:%M:%S'
    d = xldate_as_tuple(int(value), workbook.datemode)
    dt = datetime.datetime(*d)
    t = datetime.timedelta(days=(value-int(value)))
    dt = dt + t
    return dt

cellTypes = {
    xlrd.XL_CELL_BLANK : 'BLANK',
    xlrd.XL_CELL_BOOLEAN : 'BOOLEAN',
    xlrd.XL_CELL_DATE : 'DATE',
    xlrd.XL_CELL_EMPTY : 'EMPTY',
    xlrd.XL_CELL_ERROR : 'ERROR',
    xlrd.XL_CELL_NUMBER : 'NUMBER',
    xlrd.XL_CELL_TEXT : 'TEXT',
}

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

                o = None
                v = s.cell(r,c).value
                t = s.cell(r,c).ctype
                if t == 3: #date
                    v = dateFixer(wb,v)
                if formulas:
                    v = s.cell(r,c).value
                col = {
                    '@number'   : '%d'%c,
                    '@type'     : '%s'%cellTypes[t],
                    '#text'     : '%s'%v
                }
                if o:
                    col['@origin'] = '%s'%o
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

def dict2md(js):
    sio = StringIO.StringIO()

    sheets = js['workbook']['sheet']
    if type(sheets) is not list:
        sheets = [ sheets ]

    for s in sheets:

        sio.write('\n# %s\n\n'%s['@name'])

        if 'row' not in s.keys():
            continue
        rows = s['row']
        if type(rows) is not list:
            rows = [ rows ]

        headers = None
        lengths = None
        values = None
        
        for row in range(len(rows)):
            r = rows[row]
            if '@number' in r.keys():
                row = int(r['@number'])
                
            if 'col' not in r.keys():
                continue
            cols = r['col']
            if type(cols) is not list:
                cols = [ cols ]

            if not headers:
                headers = dict()
                lengths = dict()
                for col in cols:
                    text = col['#text']
                    num = 'c%s'%col['@number']
                    headers[num] = text
                    lengths[num] = len(text)
                values = list()
            else:
                value = dict.fromkeys(headers.keys())
                for col in cols:
                    num = 'c%s'%col['@number']
                    text = col['#text'].replace('\r','').replace('\n','<br/>').replace('*','\*')
                    value[num] = text
                    if len(text) > lengths[num]:
                        lengths[num] = len(text)
                values.append(value)
                        
        #print headers
        fmt = '|'.join(map(lambda x: '{%s:<%d}'%(x,lengths[x]), sorted(lengths.keys())))
        #print fmt
        sio.write('|%s|\n'%fmt.format(**headers))
        underlines = dict((x,'-'*lengths[x]) for x in lengths.keys())
        #print underlines
        sio.write('|%s|\n'%fmt.format(**underlines))
        for value in values:
            sio.write('|%s|\n'%fmt.format(**value))
            
    return sio.getvalue()

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

    if args.output.lower().endswith('md'):
        output.write(dict2md(js))
        
    output.close()
        
    return


if __name__ == '__main__': main()

