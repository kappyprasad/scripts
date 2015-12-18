#!/usr/bin/env python

import os,sys,re,requests,json

base='http://169.254.169.254/latest/meta-data'

def get(path):
    response = requests.get('%s/%s'%(base,path))
    return response.text

def main():
    keys = get('').split('\n')

    data = {}
    for key in keys:
        data[key] = get(key)

    json.dump(data,sys.stdout,indent=4)
        
if __name__ == '__main__': main()

        
    


