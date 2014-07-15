#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


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
