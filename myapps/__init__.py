from loguru import logger as log
import requests

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



def loop(host, key, verbose=False, one=False, hook=None, event=None, message=None, room=None, insecure=False):
    global locker

    locker = LockerClient(host=host, key=key, insecure=insecure)

    log.remove()
    if verbose:
        log.add(sys.stderr, colorize=True, format="{time:HH:MM:SS} <green>{message}</green>", level="DEBUG")
    else:
        log.add(sys.stderr, colorize=True, format="{time:HH:MM:SS} <green>{message}</green>", level="INFO")
    log.debug("verbose mode")


    s = Sleep(hook=hook)

    if one:
        run()
    else:
        socketio = SocketIO(message_queue="redis://")
        while True:
            userlist = run()
            for u in userlist:
                roomname = room.format(u=u)
                print(f"notify user {u} in {roomname}")
                socketio.emit(event, message, room=roomname)
            s.sleep(300)
