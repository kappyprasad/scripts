#!/usr/bin/env python

import os,sys,re,requests,json

base='http://169.254.169.254/latest'

def get(base,path):
    #sys.stderr.write('base="%s" path="%s"\n'%(base,path))
    response = requests.get('%s/%s'%(base,path))
    data = {}
    if path.endswith('/'):
        for key in response.text.split('\n'):
            data[key] = get('%s/%s'%(base,path),key)
    else:
        data = response.text
    return data

def main():
    data = get(base,'meta-data/')
    json.dump(data,sys.stdout,indent=4)
        
if __name__ == '__main__': main()

        
    


