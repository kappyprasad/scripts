#!/usr/bin/python

import sys,re,os,argparse,json,requests
from requests.auth import HTTPBasicAuth

baseurl  ='https://api.github.com'
apiurl   ='https://api.github.com/repos/'
cloneurl ='git@github.com:'

parser = argparse.ArgumentParser(description='github repository listerer')

parser.add_argument('-v', '--verbose',       action='store_true', help='show verbose detail')
parser.add_argument('-o', '--output',        action='store',      help='output file')
parser.add_argument('-u', '--username',      action='store',      help='fake user name')
parser.add_argument('-p', '--password',      action='store',      help='fake pass word')
parser.add_argument('-t', '--tag',           action='store',      help='query tag per row')
parser.add_argument(      'path',            action='store',      help='api.github.com query path')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

if 'COLUMNS' in os.environ.keys():
    horizontal = '-'*int(os.environ['COLUMNS'])
else:
    horizontal = '-'*80
    
#########################################################################################
def main():

    if args.username and args.password:
        auth=HTTPBasicAuth(args.username,args.password)
    else:
        auth=None

    headers = {
        'Accept' : 'application/json'
    }

    url='%s/%s'%(baseurl,args.path.lstrip('/'))

    repos = requests.get(url=url,auth=auth,headers=headers)
    if args.tag:
        for row in repos.json():
            print row[args.tag]
    else:
        json.dump(repos.json(),sys.stdout,indent=4)
    return

if __name__ == '__main__': main()
