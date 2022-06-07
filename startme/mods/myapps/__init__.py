from startme import StartMeThread
from myapps import loop
import os


class StartMeMyApps(StartMeThread):
    def code(self):
        host = os.getenv('MYAPPS_HOST')
        key = os.getenv('MYAPPS_KEY')
        verbose=True
        insecure=False
        hook = os.getenv('MYAPPS_HOOK', 'redis').split(' ')
        event = os.getenv('MYAPPS_EVENT', 'update')
        message = os.getenv('MYAPPS_MESSAGE')
        room = os.getenv('MYAPPS_ROOM', 'myapps-{u}')

        print(f"{self}: {host=} {hook=} {event=} {message=} {room=}")
        loop(host = host, key = key, verbose=verbose, insecure=insecure, 
            one=False, hook=hook, event=event, message=message, room=room)
