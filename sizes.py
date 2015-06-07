#!/usr/bin/env python2.7

import sys,os,re

re_app=re.compile('^(.*)\.app$')
links='/var/root/Applications'
apps='/var/mobile/Applications'

def getImage(path):
	file = '%s/iTunesArtwork'%path
	if not os.path.isfile(file):
		print '%s not found'%file
		return None
	return file

def getSize(path):
	(fi,fo,fe) = os.popen3('du.pl -q %s'%path)
	fi.close()
	size = fo.readline().rstrip()
	fo.close()
	fe.close()
	return size

def getName(path):
	key = 'itemName'
	name = None
	info = None
	file = '%s/iTunesMetadata.plist'%path
	if not os.path.isfile(file):
		return None
	(fi,fo,fe) = os.popen3('plutil -key %s %s'%(key,file))
	fi.close()
	name=fo.readline().rstrip()
	fo.close()
	fe.close()
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
	# create missing links
	for path in getApps():			
		name=getApp(path)
		size=getSize(path)
		if name and size:
			sys.stdout.write('%s %s\n'%(size, name))
			sys.stdout.flush()
					
	return	

if __name__ == '__main__':
	main()


