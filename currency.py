#!/usr/bin/env python

import sys, os, re, requests, json, argparse, logging

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',  action='store_true')
    parser.add_argument('-k','--key',      action='store',  default='082e15bd1fbaf4aca090d7108724589c')
    parser.add_argument('-u','--url',      action='store',  default='http://www.apilayer.net/api')

    parser.add_argument('-f', '--fr',      action='store',  help='from currency', default='AUD')
    parser.add_argument('-t', '--to',      action='store',  help='to currency',   default='EUR')
    parser.add_argument('-a', '--amount',  action='store',  help='ammount',       default=1, type=float)

    parser.add_argument('-l', '--list',    action='store_true')

    return parser.parse_args()

def urlify(url,data):
    url='%s?%s'%(url,'&'.join(map(lambda x : '%s=%s'%(x,data[x]), data.keys())))
    logger.debug('url=%s',url)
    return url

def quote(data,base):
    url = urlify(base,data)
    
    response = requests.get(url,data=data)
    js = response.json()
    logger.debug('js=%s',json.dumps(js,indent=4))
        
    quotes=js['quotes']
    for key in quotes.keys():
        price = quotes[key]
        del quotes[key]
        quotes[key[3:]] = price

    logger.debug('quotes=%s',json.dumps(quotes,indent=4))

    if args.fr and args.to and args.amount:
        logger.debug('USD2%s=%s USD2%s=%s',args.fr,quotes[args.fr], args.to, quotes[args.to])
        other = args.amount * quotes[args.fr] / quotes[args.to]
        print other
        
    return

def list(data,base):
    url = urlify(base,data)
    response = requests.get(url,data=data)
    js = response.json()
    logger.debug('js=%s',json.dumps(js,indent=4))
    currencies = js['currencies']
    print json.dumps(currencies,indent=4)

    return

def main():
    global args,logger

    args = argue()

    logging.basicConfig()
    logger=logging.getLogger(__name__)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.debug('args=%s',json.dumps(vars(args),indent=4))

    data={
        'access_key': args.key,
        'format' : 1,
    }

    if args.list:
        list(data,'%s/list'%args.url)
    else:
        quote(data,'%s/live'%args.url)
    
    return
    

if __name__ == '__main__': main()




