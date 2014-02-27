#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/send-wssc.py $
# $Id: send-wssc.py 7279 2013-12-12 14:22:40Z david.edson $

import sys, re, os, urllib, urllib2, argparse, StringIO

from _tools.parser import *
from _tools.xpath import *
from _tools.eddo import *
from _tools.cdata import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-c','--colour',   action='store_true', help='show in colour')
parser.add_argument('-u','--username', action='store',      help='fake user name')
parser.add_argument('-p','--password', action='store',      help='fake pass word')
parser.add_argument('-o','--output',   action='store',      help='output file')
parser.add_argument('wssc',  action='store',                help='the wssc file')
parser.add_argument('param', action='store', nargs='*',     help='the wssc parameters')

args = parser.parse_args()

if args.verbose:
    nestPrint(vars(args),colour=True,output=sys.stderr)

def main():
    colour = args.colour
    verbose = args.colour
    output = args.output
    horizon = buildHorizon()

    credentials = {}
    if args.username and args.password:
        credentials['username'] = args.username
        credentials['password'] = args.password

    (doc,ctx) = getContextFromFile(args.wssc)
    url = getElementText(ctx,'/SOAP-CALL/SOAP-FIELDS/URL')
    soapAction = getElementText(ctx,'/SOAP-CALL/SOAP-FIELDS/action')
    soapBody = '%s'%getElement(ctx,'/SOAP-CALL/REQUEST').content

    if soapBody:
        sbi = StringIO.StringIO(soapBody)
        sbo = StringIO.StringIO()
        cdata2xml(sbi,sbo)
        soapBody = sbo.getvalue()
        sbo.close()

    if args.param:
        for i in range(len(args.param)):
            soapBody = soapBody.replace('$%d'%(i+1),args.param[i])

    sbh = []
    sbp = re.compile('.*\$\d.*')
    for line in soapBody.split('\n'):
        if sbp.match(line):
            sbh.append(line)

    if len(sbh) > 0:
        print 'usage: %s'%sys.argv[0]
        for line in sbh:
            print line
        return

    headers = {
        'SOAPAction'     : '"%s"'%soapAction,
        'Content-Type'   : 'text/xml; charset=UTF-8',
        'Content-Length' : len(soapBody),
    }

    if verbose:
        sys.stderr.write('url=%s\n'%url)
        if len(credentials) > 0:
            sys.stderr.write('user=%s'%credentials['username'])
        for key in headers.keys():
            sys.stderr.write('#%s : %s\n'%(key,headers[key]))
        sys.stderr.write('%s\n'%horizon)
        myParser = MyParser(colour=colour,output=sys.stderr,rformat=True)
        myParser.parser.Parse(soapBody)
        del myParser

    try:
        if (len(credentials) > 0):    
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            top_level_url = url
            password_mgr.add_password(None, top_level_url, credentials['username'], credentials['password'])
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            opener.open(url)
            urllib2.install_opener(opener)
            
        data = soapBody # urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        res = urllib2.urlopen(req)
        xml = res.read()

        fp = sys.stdout
        if output:
            colour=False
            fp = open(output,'w')

        myParser = MyParser(colour=colour,rformat=True,output=fp)
        myParser.parser.Parse(xml)
        del myParser
        
        if output:
            fp.close()

    except urllib2.URLError, e:
        print 'Failed: %s'%e #e.code
        myParser = MyParser(colour=colour,output=sys.stderr,rformat=True)
        myParser.parser.Parse(e.read())
        del myParser
    except:
        print 'failed:', sys.exc_info()[0]
    

    return

if __name__ == '__main__' : main()
