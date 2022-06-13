# locker-myapps

Application manager for locker. This is main app where users of locker server create their applications.

## Install
Better to install inside virtualenv of locker-server

~~~
.  /opt/venv/locker-server/bin/activate
pip3 install git+https://github.com/yaroslaff/locker-myapps
~~~

If [startme](https://github.com/yaroslaff/startme) is installed inside locker virtualenv, it wull be started automatically with startme. Add myapps variables to `/etc/default/startme-locker` like this:
~~~
STARTME_HOOK=redis
MYAPPS_HOST=myapps.l.www-security.com
MYAPPS_KEY=MySecretKey
~~~

## Quickstart

### Create app on locker server 
You may use myapps or (if you are admin of locker server):
~~~
# username is 'my' here
sudo -u www-data locker-admin create my notebook
~~~

(copy autogenerated KEY from output, or use `--key` to specify it manually )

### Create .env file
~~~
# LOCKER_HOST is APP_NAME-USER.YOURDOMAIN
LOCKER_HOST=apps-my.ll.www-security.net
LOCKER_KEY=<Your key here>

export LOCKER_HOST
export LOCKER_KEY
~~~

Now, all further `locker-admin` commands require either LOCKER_KEY and LOCKER_HOST env variables, or must be run in directory with this `.env` file.

### Test if app is created and deploy
In same directory with .env file, run `locker-admin ls`:
~~~
$ locker-admin ls 
home/                                                       DIR mt:1640712673.841365
var/                                                        DIR mt:1640712673.841365
etc/                                                        DIR mt:1640712673.841365
~~~

deploy app (from virtualenv):
~~~
locker-admin deploy $VIRTUAL_ENV/locker_myapps/
~~~

### Configure application
Add your website URL to `origins`: `locker-admin edit etc/options.json`. Example:
~~~
{
    "origins": [
        "http://localhost:8000",
        "https://myapps.www-security.com"
    ],
    "flag-options": {
        "flags.json": {
            "notify": "redis:publish",
	        "data": "StartMeMyApps"
        }
    }
}
~~~
Make sure there MUST be NO trailing slash in origins.

### Manual run
make request to create app from web UI, then:
~~~
sudo -u www-data bin/myapps.py --one -v
~~~

### run app client-side (daemon? systemd)

### integration with ws-emit

#### Option 1: Websocket
~~~
bin/myapps.py --hook ws room=myapps url=https://rudev.www-security.net:8899/
~~~
etc/options.json:
~~~
"flag-options": {
    "flags.json": {
        "notify": "socketio",
        "room": "myapps",
        "data": "flag updated"
	}
}
~~~

#### Option 2: Redis
~~~
bin/myapps.py --hook redis
~~~

etc/options.json:
~~~
"flag-options": {
    "flags.json": {
		"notify": "redis:publish",
		"channel": "sleep",
	}
}
~~~



### Start development webserver
Run server:
~~~
locker-admin serve
~~~
