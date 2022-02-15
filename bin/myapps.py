#!/usr/bin/env python3

import argparse
from locker_client import LockerClient
import os
import sys
from dotenv import load_dotenv
import subprocess
import string
import time
import random
import requests
import datetime
import json

from flask_socketio import SocketIO

from loguru import logger as log


from lightsleep import Sleep

from requests.api import request

locker = None

def gen_key(length=40):
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    key = ''.join(random.choice(alphabet) for i in range(length))
    return key


def run():
    log.debug("Run...")
    print("Run!", locker)
    flags = locker.get_flags('/var/flags.json', 'updated')
    userlist = set()

    droplist = []
    for u, ts in flags:
        print(u, ts)        

        # get requests
        r = locker.get(f'/home/{u}/rw/requests.json')
        create_requests = r.json()

        # get app list
        try:
            r = locker.get(f'/home/{u}/r/apps.json')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                applist = dict()
        else:
            print(r)
            print(r.text)
            applist = r.json()

        print(r)
        print(r.json)

        for req in create_requests:
            app_name = req['name'].lower()

            print(f"Create app {app_name}")

            new_key = gen_key()
            rc = subprocess.run(['locker-admin','create', u, app_name, '--key', new_key])
            print(rc)
            
            app = {
                'name': app_name,
                'status': 'created',
                'created_timestamp': int(time.time()),
                'created': datetime.datetime.now().strftime('%Y/%m/%d'),
                'subtitle': 'New application',
                'details': f'Created with initial key: {new_key}'
            }   

            applist[app_name] = app

        # update create requests
        r = locker.put(f'/home/{u}/rw/requests.json', '[]')

        # update applist
        r = locker.put(f'/home/{u}/r/apps.json', json.dumps(applist, indent=4))
        droplist.append([u, ts])

        userlist.add(u)

    print(droplist)
    result = locker.drop_flags('/var/flags.json', 'updated', droplist)
    print(result)
    return userlist

def get_args():

    load_dotenv(dotenv_path='.env')

    def_key = os.getenv('LOCKER_KEY', None)
    def_host = os.getenv('LOCKER_HOST', None)
    def_event = 'update'
    def_room = 'myapps-{u}'
    def_message=''


    parser = argparse.ArgumentParser(description='Locker admin')

    g = parser.add_argument_group('Commands')
    g.add_argument('--one', default=False, 
        action='store_true', help='one run')

    g = parser.add_argument_group('Websocket event')
    g.add_argument('--event', metavar='EVENT', default=def_event,
        help=f'websocket event name. def: {def_event}')
    g.add_argument('--room', metavar='ROOM', default=def_room,
        help=f'websocket room name. def: {def_room}')
    g.add_argument('--message', metavar='MESSAGE', default=def_message,
        help=f'message text {def_message}')

    g = parser.add_argument_group('Options')
    g.add_argument('--key', metavar='KEY', default=def_key,
        help='Use this X-API-KEY header: $LOCKER_API_KEY={}'.format(def_key))
    g.add_argument('--host', metavar='HOST', default=def_host,
        help='Your locker hostname: $LOCKER_HOST={}'.format(def_host))
    g.add_argument('--insecure-ssl', default=False, action='store_true',
        help=f'Do not verify server-side certificate')
    g.add_argument('--verbose', '-v', action='store_true',  default=False,
        help='Verbose mode')
    g.add_argument('--hook', nargs='+', metavar=('METHOD', 'ARG'), help='lightsleep-hook with arguments')



    return parser.parse_args()


def main():

    global locker, log

    args = get_args()

    s = Sleep(hook=args.hook)

    log.remove()
    if args.verbose:
        log.add(sys.stderr, colorize=True, format="{time:HH:MM:SS} <green>{message}</green>", level="DEBUG")
    else:
        log.add(sys.stderr, colorize=True, format="{time:HH:MM:SS} <green>{message}</green>", level="INFO")
    log.debug("verbose mode")



    locker = LockerClient(host=args.host, key=args.key, insecure=args.insecure_ssl)

    if args.one:
        run()
    else:
        socketio = SocketIO(message_queue="redis://")
        while True:
            userlist = run()
            for u in userlist:
                roomname = args.room.format(u=u)
                print(f"notify user {u} in {roomname}")
                socketio.emit(args.event, args.message, room=roomname)
            s.sleep(300)

if __name__ == '__main__':
    main()
