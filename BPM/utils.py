#!/usr/bin/python

# $Date: 2014-06-24 18:04:17 +1000 (Tue, 24 Jun 2014) $
# $Revision: 11881 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/BPM/utils.py $
# $Id: utils.py 11881 2014-06-24 08:04:17Z david.edson $

import re,uuid

dids = {
    # did : sid
}

def fixTwxRef(sid,ref):
    if ref == None:
        return None
    cref = ref
    if len(cref) > 0 and cref[0] == '/':
        cref = '%s%s'%(sid,ref)
    elif '/' in cref:
        bits = ref.split('/')
        did = bits[0]
        cid = bits[1]
        if did in dids.keys():
            cref = '%s/%s'%(dids[did],cid)
    return cref

def fixTwxID(sid,ref):
    if ref == None:
        return None
    cref = ref.lstrip('/')
    cref = '%s/%s'%(sid,ref)
    return cref
