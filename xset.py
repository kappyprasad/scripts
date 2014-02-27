#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/xset.py $
# $Id: xset.py 7279 2013-12-12 14:22:40Z david.edson $

import sys, re, os, libxml2

from _tools.xpath import *

pp = re.compile('^.*/([^/]*)$')
pa = re.compile('^(.*)/@([^@]*)$')

def main():
    args = sys.argv[1:]

    if '-s' in args:
        s = args.index('-s')
        del args[s]
        stream = True
    else:
        stream = False

    if '-t' in args:
        t = args.index('-t')
        text = args[t+1]
        del args[t+1]
        del args[t]
    else:
        text = None

    if '-a' in args:
        a = args.index('-a')
        attr = True
        value = args[a+1]
        del args[a+1]
        del args[a]
    else:
        attr = None

    ns = {}
    pn = re.compile('^([^:]*):(.*)$');
    while '-n' in args:
        n = args.index('-n')
        v = args[n+1]
        del args[n+1]
        del args[n]
        m = pn.match(v)
        if m:
            ns[m.group(1)]=m.group(2)

    if len(args) < 2:
        m = pp.match(sys.argv[0])
        print 'usage: %s <xpath> -[ta] <value> <files*>'%m.group(1)
        return

    xpath=args[0]

    if attr:
        m = pa.match(xpath)
        xpath = m.group(1)
        attr = m.group(2)

    for f in args[1:]:
        if stream:
            b = f
        else:
            b='%s.bak'%f
            try:
                os.remove(b)
            except:
                None
            os.rename(f,b)

        
        (doc,ctx)=getContextFromFile(b)
        for p in ns.keys():
            ctx.xpathRegisterNs(p,ns[p])

        res = ctx.xpathEval(xpath)
        for r in res:
            if text:
                r.setContent(text)
            if attr:
                r.setProp(attr,value)

        if stream:
            print '%s'%doc
        else:
            output = open(f,'w')
            output.write('%s'%doc)
            output.close()
    return

if __name__ == '__main__' : main()
