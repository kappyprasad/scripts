#!/usr/bin/env python

# https://wiki.openoffice.org/wiki/Documentation/How_Tos/Calc:_SUBTOTAL_function

import os,sys,re,json,argparse,requests,urllib3

from datetime import *

from xlrd import open_workbook
from xlwt import Workbook,Formula,XFStyle

from requests.auth import HTTPBasicAuth

# git@github.com:eddo888/Tools.git
from Tools.Squirrel import Squirrel

squirrel = Squirrel()

urllib3.disable_warnings()

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',   action='store_true')
    parser.add_argument('-U','--username',  action='store',      default='eddo888@tpg.com.au')
    parser.add_argument('-H','--hostname',  action='store',      default='jira.atlassian.com')
    parser.add_argument('-i','--input',     action='store',      help='input file')
    parser.add_argument('-o','--output',    action='store',      help='output file')
    parser.add_argument('-k','--keys',      action='store',      default='keys.json')

    group1=parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-j','--jsonI',     action='store_true', help='json format for input')
    group1.add_argument('-e','--xlsI',      action='store_true', help='xls format for input')
    
    group2=parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-J','--jsonO',     action='store_true', help='json format for output')
    group2.add_argument('-T','--textO',     action='store_true', help='text format for output')
    group2.add_argument('-E','--xlsO',      action='store_true', help='xls format for output')

    group3=parser.add_mutually_exclusive_group(required=True)
    group3.add_argument('-q','--query',     action='store_true', help='query')
    group3.add_argument('-u','--upload',    action='store_true', help='upload')

    args = parser.parse_args()

    if args.verbose:
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')

    return args


def query(input,output,args):
    jql = input.read().replace('\n','')
    
    headers= {
        'Accept'       : 'application/json',
        'Content-Type' : 'application/json',
    }

    data={ 
        'jql': '%s'%jql,
        'startAt' : 0,
        'maxResults' : 1000
    }

    if args.verbose:
        json.dump(data,sys.stderr,indent=4)
        sys.stderr.write('\n')

    password = squirrel.get('%s:jira:%s'%(args.hostname,args.username))
    auth=HTTPBasicAuth(args.username,password)

    path='rest/api/2/search'

    url='https://%s/%s'%(args.hostname,path)


    format=' '.join(
        map(
            lambda x : 
                x['format'],
                keys
        )
    )

    response = requests.post(
        url, 
        headers=headers,
        data=json.dumps(data),
        auth=auth
    )

    if args.verbose:
        sys.stderr.write('%s\n'%response)
        sys.stderr.write('%s\n'%response.json())
        
    if args.xlsO:
        workbook = Workbook()
        sheet = workbook.add_sheet('Query')
        for i in range(len(keys)):
            sheet.col(i).width = 256*keys[i]['width']
            sheet.write(0,i,keys[i]['name'])
    if args.textO:
        output.write('%s\n'%format.format(
            *map(
                 lambda x : 
                     x['name'],
                     keys
            )
        ))

    dividers = {
        1       : 'Minutes',
        60*60   : 'Hours',
        60*60*8 : 'Days',
    }

    dts = '%Y-%m-%dT%H:%M:%S'
    
    if response:
        rows = 0
        js = response.json()

        if args.jsonO:
            json.dump(js,output,indent=4)
        else:
            for issue in js['issues']:
                rows = rows + 1
                cols = values(issue)
                if args.xlsO:
                    for i in range(len(cols)):
                        val = cols[i]
                        if keys[i]['path'] == 'key':
                            val = Formula('HYPERLINK("https://%s/browse/%s";"%s")'%(args.hostname,val,val))
                        if 'style' in keys[i].keys():
                            style = XFStyle()
                            style.num_format_str = keys[i]['style']
                            try:
                                val = val.rstrip('.000+1000')
                                val = datetime.strptime(val,dts)
                                sheet.write(rows,i,val,style)
                            except:
                                None
                        else:
                            sheet.write(rows,i,val)
                if args.textO:
                    output.write('%s\n'%format.format(*cols))

        srows=rows

        for divider in sorted(dividers.keys()):
            
            rows = rows + 1

            if args.xlsO:
                sheet.write(rows,0,dividers[divider])
                for i in range(len(keys)):
                    if 'sum' not in keys[i].keys():
                        continue
                    col = chr(ord('A')+i)
                    formula = 'subtotal(9;%s%d:%s%d)/%d'%(
                       col,2,col,srows,divider
                    )
                    #print i,rows,col,formula
                    sheet.write(rows,i,Formula(formula))
            if args.textO:
                output.write('%s\n'%format.format(
                    *map(
                         lambda x : 
                             x['sum']/divider if 'sum' in x.keys() else '',
                             keys
                    )
                ))

        if args.xlsO:
            workbook.save(output)
    return

def upload(input,output,args):
    data = json.load(input)
    
    headers= {
        'Accept'       : 'application/json',
        'Content-Type' : 'application/json',
    }

    if args.verbose:
        json.dump(data,sys.stderr,indent=4)
        sys.stderr.write('\n')

    password = Passwords(args.hostname,args.username).password
    auth=HTTPBasicAuth(args.username,password)

    path='rest/api/2/issue'

    url='https://%s/%s'%(args.hostname,path)

    response = requests.post(
        url, 
        headers=headers,
        data=json.dumps(data),
        auth=auth
    )

    if args.verbose:
        sys.stderr.write('%s\n'%response)
        sys.stderr.write('%s\n'%response.json())
        
    if args.xlsI:
        workbook = Workbook()
        sheet = workbook.add_sheet('Query')
        for i in range(len(keys)):
            sheet.col(i).width = 256*keys[i]['width']
            sheet.write(0,i,keys[i]['name'])
    else:
        None
        
    if response:
        rows = 0
        js = response.json()

        if args.xlsI:
            workbook.save(output)
        if args.jsonO:
            json.dump(js,output,indent=4)
            
    return

def value(issue,key):
    expression = '["%s"]'%'"]["'.join(key.split('.'))
    try:
        v = eval('issue%s'%expression)
    except:
        v = None
    if not v:
        v=''
    return v

def values(issue):
    vs = []
    for key in keys:
        v = value(issue,key['path'])
        if v and 'sum' in key.keys():
            key['sum'] += int(v)
        vs.append(v)
    return tuple(vs)


def main():
    global keys
    
    args = argue()

    with open(args.keys) as k:
        keys = json.load(k)
        
    if args.input:
        input = open(args.input)
    else:
        input = sys.stdin

    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout
        
    if args.query:
        query(input,output,args)
    if args.upload:
        upload(input,output,args)

    return

if __name__ == '__main__': main()
