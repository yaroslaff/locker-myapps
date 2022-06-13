from startme import StartMe
from locker_client import LockerClient
from myapps import run
import os
from flask_socketio import SocketIO
from startme import StartMeDisabled


class StartMeMyApps(StartMe):
    def __init__(self):
        self.host = os.getenv('MYAPPS_HOST')
        self.key = os.getenv('MYAPPS_KEY')
        self.verbose=True
        self.insecure=False

        self.event = os.getenv('MYAPPS_EVENT', 'update')
        self.message = os.getenv('MYAPPS_MESSAGE')
        self.room = os.getenv('MYAPPS_ROOM', 'myapps-{u}')

        self.period = 60
        self.socketio = SocketIO(message_queue="redis://")

        # sanity checks
        if not self.host:
            print('set MYAPPS_HOST env variable')
            raise StartMeDisabled
        if not self.key:
            print('set MYAPPS_KEY env variable')
            raise StartMeDisabled


        self.locker = LockerClient(host=self.host, key=self.key, insecure=self.insecure)


        #print(f"{self}: {self.host=} {self.hook=} {self.event=} {self.message=} {self.room=}")
        #loop(host = host, key = key, verbose=verbose, insecure=insecure, 
        #    one=False, hook=hook, event=event, message=message, room=room)

    def on_start(self):
        print(self, "on_start()")

    def on_schedule(self):
        print(self, "on_schedule()")
        self.run()
    
    def run(self):
        userlist = run(self.locker)
        for u in userlist:
            roomname = self.room.format(u=u)
            print(f"notify user {u} in {roomname}")
            self.socketio.emit(self.event, self.message, room=roomname)
