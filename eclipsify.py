#!/usr/bin/env python

import os,sys,re,json,argparse,xmltodict,logging,shutil

def argue():
    parser = argparse.ArgumentParser('Tool to create python eclipse .project etal')
    parser.add_argument('-v','--verbose', action='store_true')
    parser.add_argument('dirs', action='store',  nargs='*', help='the directories, defaults to .')

    
    args = parser.parse_args()
    if args.verbose: sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))
    return args

def main():
    args = argue()
    level=logging.INFO
    if args.verbose:
        level=logging.DEBUG
    logging.basicConfig(level=level)
    source=os.path.dirname(sys.argv[0])
    logging.debug('source=%s\n'%source)
    dirs = args.dirs
    if len(dirs) == 0:
        dirs.append('.')

    for dir in dirs:
        dir = dir.rstrip('/')
        logging.debug('dir=%s\n'%dir)

        target=os.path.abspath(dir)
        target=target[target.rfind('/')+1:]
        
        shutil.copy('%s/.pydevproject'%source,'%s/'%dir)

        with open('%s/.project'%source) as fp:
            project = xmltodict.parse(fp)
        project['projectDescription']['name'] = target
        project['projectDescription']['comment'] = target

        with open('%s/.project'%dir,'w') as fp:
            xmltodict.unparse(project,output=fp,indent='    ',pretty=True)

        logging.info('target=%s\n'%target)
        
    return


if __name__ == '__main__': main()
