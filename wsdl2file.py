#!/usr/bin/env python

import os,sys,re,json,argparse,logging,requests

from Tools.xpath import *

def argue():
    parser = argparse.ArgumentParser('download wsdl and imports')

    parser.add_argument('-v','--verbose',    action='store_true')
    parser.add_argument('-u','--username',   action='store',       help='your user name')
    parser.add_argument('-p','--password',   action='store',       help='your pass word')
    parser.add_argument('-d','--directory',  action='store',       default='.wsdl')
    parser.add_argument('wsdl',               action='store')
    
    args = parser.parse_args()
    if args.verbose:
        sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))
    return args

def download(url):
    print url
    
    auth=None
    if args.username and args.password:
        auth=(args.username,args.password)

    headers = {
        'Content-Type' : 'text/xml'
    }
    
    response = requests.get(url,auth=auth,headers=headers)
    print response
    xml = response.text
    
    del response
    del headers
    del auth
    
    name = os.path.basename(url)
    print name

    if not name in names.keys():
        names[name] = 0
    else:
        names[name] += 1
        
    f = '%s/%s.%s'%(args.directory,names[name],name)

    with open(f,'w') as fo:
        fo.write(xml)
        fo.close()

    (doc,ctx,nsp) = getContextFromStringWithNS(xml,None)

    xsp = 'xs'
    xsd = 'http://www.w3.org/2001/XMLSchema'
    ctx.xpathRegisterNs(xsp,xsd)

    print json.dumps(nsp,indent=4)
    
    r = doc.getRootElement()
    
    children = []

    for xi in ctx.xpathEval('//xs:import') + ctx.xpathEval('//xs:include'):
        child = getAttribute(xi,'schemaLocation')
        if child:
            children.append(child)

    if r.name == 'definitions':
        for si in ctx.xpathEval('//xs:schema'):
            si.unlinkNode()
            setAttribute(si,'xmlns:tns',getAttribute(si,'targetNamespace'))
            p = re.compile('^ xmlns:([^=]*)=["\']([^\'"]*)["\']$')
            s = str(si.ns())
            #print s
            m = p.match(s)
            if m:
                #print m.groups()
                setAttribute(si,'xmlns:%s'%m.group(1),m.group(2))

            for p in nsp.keys():
                if p != 'tns':
                    setAttribute(si,'xmlns:%s'%p,nsp[p])
                    
            f = '%s/%s.xsd'%(args.directory,getAttribute(si,'targetNamespace'))
            print f
            with open(f,'w') as fo:
                fo.write(str(si))
                fo.close()
    
    del doc
    del ctx

    for child in children:
        download(child)
        
    return

def main():
    global args,names
    args = argue()
    names = {}
    
    level=logging.INFO
    if args.verbose:
        level=logging.DEBUG
        
    logging.basicConfig(level=level)

    if not os.path.isdir(args.directory):
        os.makedirs(args.directory)

    download(args.wsdl)
    return


if __name__ == '__main__': main()


