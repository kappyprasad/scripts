#!/usr/bin/python

import sys,os,re
import plistlib

re_app=re.compile('^(.*)\.app$')
links='/var/root/Applications'
apps='/var/mobile/Applications'

def getImage(path):
    file = '%s/iTunesArtwork'%path
    if not os.path.isfile(file):
        print '%s not found'%file
        return None
    return file
        
def getName(path):
    key = 'itemName'
    name = None
    info = None
    file = '%s/iTunesMetadata.plist'%path
    if not os.path.isfile(file):
        return None
    fi = open(file,'rb')
    pl = plistlib.readPlist(fi)
    fi.close()
    name=pl[key]
    name = name.replace('/','')
    return name

def getApp(path):
    for file in os.listdir(path):
        m = re_app.match(file)
        if m:
            return m.group(1)
    return None 

def getApps():
    paths = []
    for file in os.listdir(apps):
        path = '%s/%s'%(apps,file)
        if os.path.isdir(path):
            paths.append(path)
    return paths
    
def getLinks():
    paths = []
    for file in os.listdir(links):
        path = '%s/%s'%(links,file)
        if os.path.islink(path):
            paths.append(path)
    return paths
        
def main():
    # remove stale links
    for link in getLinks():
        if not os.path.exists(link):
            print '-%s'%os.path.basename(link)
            os.unlink(link)
            
    # create missing links
    for path in getApps():            
        name=getApp(path)
        if name:
            link = '%s/%s'%(links,name)
            if not os.path.exists(link):
                print '+%s'%(name)
                os.symlink(path,link)
            else: 
                None    
                #print '=%s'%(name)
                    
    return    

if __name__ == '__main__':
    main()


