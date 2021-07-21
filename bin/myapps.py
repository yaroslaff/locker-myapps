#!/usr/bin/env python3

import argparse
from locker_client import LockerClient
import os

locker = None

def run():
    print("Run!", locker)
    flags = locker.get_flags('/var/flags.json', 'updated')

    droplist = []
    for u, ts in flags:
        print(u, ts)
        droplist.append([u, ts])
    print(droplist)
    result = locker.drop_flags('/var/flags.json', 'updated', droplist)
    print(result)

def get_args():
    def_key = os.getenv('LOCKER_KEY', None)
    def_host = os.getenv('LOCKER_HOST', None)

    parser = argparse.ArgumentParser(description='Locker admin')

    g = parser.add_argument_group('Commands')
    g.add_argument('--one', default=False, 
        action='store_true', help='one run')

    g = parser.add_argument_group('Options')
    g.add_argument('--key', metavar='KEY', default=def_key,
        help='Use this X-API-KEY header: $LOCKER_API_KEY={}'.format(def_key))
    g.add_argument('--host', metavar='HOST', default=def_host,
        help='Your locker hostname: $LOCKER_HOST={}'.format(def_host))
    g.add_argument('--insecure-ssl', default=False, action='store_true',
        help=f'Do not verify server-side certificate')

    return parser.parse_args()


def main():

    global locker

    args = get_args()

    locker = LockerClient(host=args.host, key=args.key, insecure=args.insecure_ssl)

    if args.one:
        run()

if __name__ == '__main__':
    main()
