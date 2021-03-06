#!/usr/bin/env python

import os,sys,re,json,argparse,urllib

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',action='store_true')
    parser.add_argument('-r','--recurse',action='store_true',help='recurse dirs')
    parser.add_argument('-o','--output',action='store',help='output file name',default='index.html')
    parser.add_argument('-d','--directory',action='store',help='the file name', default=".")

    args = parser.parse_args()

    if args.verbose:
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')

    return args

def directory(dir,output,target,recurse=False):
    for file in os.listdir('%s'%dir):
        path='%s/%s'%(dir,file)
        if os.path.isfile(path):
            if file != target and file[0] != '.':
                output.write('<a href="%s">%s</a><br/>\n'%(urllib.quote(path),path))
        if os.path.isdir(path):
            output.write('<a href="%s/index.html">%s</a><br/>\n'%(urllib.quote(path),path))
            if recurse:
                directory('%s/%s'%(dir,file),output,target,recurse)
    return

def main():
    args = argue()
    if args.output:
        output=open(args.output,'w')
    else:
        output=sys.stdout

    output.write('<html><body>\n')
    directory(args.directory,output,args.output,args.recurse)
    output.write('</body></html>')
    
    if args.output:
        output.close()
        
    return

if __name__ == '__main__': main()

