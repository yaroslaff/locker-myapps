from startme import StartMe
from myapps import run
import os
from flask_socketio import SocketIO


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

        #print(f"{self}: {self.host=} {self.hook=} {self.event=} {self.message=} {self.room=}")
        #loop(host = host, key = key, verbose=verbose, insecure=insecure, 
        #    one=False, hook=hook, event=event, message=message, room=room)

    def on_start(self):
        print(self, "on_start()")

    def on_schedule(self):
        print(self, "on_schedule()")
        self.run()
    
    def run(self):
        while True:
            userlist = run()
            for u in userlist:
                roomname = self.room.format(u=u)
                print(f"notify user {u} in {roomname}")
                self.socketio.emit(self.event, self.message, room=roomname)
