#!/usr/bin/env python

import sys, os, re, requests, json, argparse, logging

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',  action='store_true')
    parser.add_argument('-k','--key',      action='store',  default='082e15bd1fbaf4aca090d7108724589c')
    parser.add_argument('-u','--url',      action='store',  default='http://www.apilayer.net/api/live')

    parser.add_argument('-f', '--from',    action='store',  default='AUD')
    parser.add_argument('-t', '--to',      action='store',  default='EUR')
    parser.add_argument('-a', '--amount',  action='store',  default=1)

    #parser.add_argument('-c', '--currency',action='store_true')

    return parser.parse_args()

def main():
    args = argue()

    if args.verbose:
        level=logging.DEBUG
    else:
        level=logging.INFO
        
    logging.basicConfig(level=level)

    
    logging.debug('args=%s',json.dumps(vars(args),indent=4))

    data={
        'access_key': args.key,
        'format' : 1,
    }

    url='%s?%s'%(args.url,'&'.join(map(lambda x : '%s=%s'%(x,data[x]), data.keys())))
    logging.debug('url=%s',url)

    response = requests.get(url,data=data)
    js = response.json()
    logging.debug('js=%s',json.dumps(js,indent=4))
        
    quotes=js['quotes']
    for key in quotes.keys():
        price = quotes[key]
        del quotes[key]
        quotes[key[3:]] = price

    logging.debug('quotes=%s',json.dumps(quotes,indent=4))
        
    return

if __name__ == '__main__': main()




