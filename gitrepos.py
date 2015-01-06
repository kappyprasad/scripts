#!/usr/bin/python

import sys,re,os,argparse,json,requests
from subprocess import Popen, PIPE
from requests.auth import HTTPBasicAuth

baseurl  ='https://api.github.com'
apiurl   ='https://api.github.com/repos/'
cloneurl ='git@github.com:'
clonetag ='clone_url'

parser = argparse.ArgumentParser(description='github repository listerer')

parser.add_argument('-v', '--verbose',   action='store_true', help='show verbose detail')
parser.add_argument('-u', '--user',      action='store',      help='github username')
parser.add_argument('-p', '--pswd',      action='store',      help='github password')

group1=parser.add_mutually_exclusive_group(required=True)
group1.add_argument('-o', '--ownr',      action='store',      help='list repos for owner')
group1.add_argument('-c', '--cpny',      action='store',      help='list repos for company')
#group1.add_argument('-r', '--repo',      action='store',      help='clone the repo')


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
def list(auth,headers,url):
    repos = requests.get(url=url,auth=auth,headers=headers)
    for row in repos.json():
        if type(row) == dict and clonetag in row.keys():
            if args.verbose:
                json.dump(row,sys.stderr,indent=4)
            print row[clonetag]
    return

#########################################################################################
def get(repo):
    print repo
    return

#########################################################################################
def main():

    if args.user and args.pswd:
        auth=HTTPBasicAuth(args.user,args.pswd)
    else:
        auth=None

    headers = {
        'Accept' : 'application/json'
    }

    if args.ownr: list(auth,headers, url='%s/users/%s/repos'%(baseurl,args.ownr))
    if args.cpny: list(auth,headers, url='%s/orgs/%s/repos'%(baseurl,args.cpny))
    if args.repo: get(args.repo)
    
    return

if __name__ == '__main__': main()
