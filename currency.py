#!/usr/bin/env python

import sys, os, re, requests, json, argparse, logging

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',  action='store_true')
    parser.add_argument('-k','--key',      action='store',  default='082e15bd1fbaf4aca090d7108724589c')
    parser.add_argument('-u','--url',      action='store',  default='http://www.apilayer.net/api/live')

    parser.add_argument('-f', '--fr',      action='store',  help='from currency', default='AUD')
    parser.add_argument('-t', '--to',      action='store',  help='to currency',   default='EUR')
    parser.add_argument('-a', '--amount',  action='store',  help='ammount',       default=1)

    #parser.add_argument('-c', '--currency',action='store_true')

    return parser.parse_args()

def main():
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

    url='%s?%s'%(args.url,'&'.join(map(lambda x : '%s=%s'%(x,data[x]), data.keys())))
    logger.debug('url=%s',url)

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
        logger.info('from=%s to=%s',quotes[args.fr], quotes[args.to])
        other = args.amount * quotes[args.fr] / quotes[args.to]
        print other
        
    return

if __name__ == '__main__': main()




