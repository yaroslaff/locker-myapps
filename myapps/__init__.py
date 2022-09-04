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


def run(locker):
    print(f"Run... {locker}")
    flags = locker.get_flags('/var/flags.json', 'updated')
    userlist = set()

    droplist = []
    for u, ts in flags:
        print(u, ts)        

        # get requests
        r = locker.get(f'/home/{u}/rw/requests.json')
        cmd_requests = r.json()

        # get app list
        try:
            r = locker.get(f'/home/{u}/r/apps.json')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                applist = dict()
        else:
            applist = r.json()

        for req in cmd_requests:
            print("REQUEST:", req)
            app_name = req['name'].lower()
            cmd = req['command']

            if cmd == 'create_app':
                print(f"Create app {u}:{app_name}")

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
            elif cmd == 'delete_app':
                if app_name in applist:
                    print(f"Delete app {u}:app_name")
                    rc = subprocess.run(['locker-admin', 'delete', u, app_name])
                    del applist[app_name]
                    print(rc)
                else:
                    print(f"Do not see {app_name} in applist")
            else:
                print(f"Do not know how to make command {cmd}")

        # update create requests
        r = locker.put(f'/home/{u}/rw/requests.json', '[]')

        # update applist
        r = locker.put(f'/home/{u}/r/apps.json', json.dumps(applist, indent=4))
        droplist.append([u, ts])
        
        userlist.add(u)

    result = locker.drop_flags('/var/flags.json', 'updated', droplist)
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
        run(locker)
    else:
        socketio = SocketIO(message_queue="redis://")
        while True:
            userlist = run(locker)
            for u in userlist:
                roomname = room.format(u=u)
                print(f"notify user {u} in {roomname}")
                socketio.emit(event, message, room=roomname)
            s.sleep(300)

