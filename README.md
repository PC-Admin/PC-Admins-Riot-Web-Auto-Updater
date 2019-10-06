
# PC-Admin's Riot Web Auto Updater


This is a script i wrote to automatically and securely update the riot-web code on nginx with customisations.

Contact me at: @PC-Admin:perthchat.org if you get stuck or have an edit in mind.

***
## Licensing

This work is licensed under Creative Commons Attribution Share Alike 4.0, for more information on this license see here: https://creativecommons.org/licenses/by-sa/4.0/

***
## Setup script

$ mkdir ~/autoupdateriot

$ mkdir ~/autoupdateriot/tocopy

$ touch ~/autoupdateriot/update_riot.log

Place the autoupdateriot.py script into ~/autoupdateriot, go through the script and replace 'username' with your desired username.

Place your own custom config.json for riot into ~/autoupdateriot/tocopy

Configure Visudo to allow the chosen username to complete like so:

```
# Cmnd alias specification
Cmnd_Alias AUTOUPDATERIOT = /bin/rm -r /usr/share/nginx/html/*, /bin/cp -r * /usr/share/nginx/html/

# username on this host can run commands as root without a password:
username ALL = (root) NOPASSWD: AUTOUPDATERIOT
```

***
## Install beautifulsoup4

Install beautifulsoup4 with:

$ sudo apt install python3-pip

$ pip3 install beautifulsoup4

***
## Crontab Setup

This updates the code every week.

Needs crontab:

@weekly /usr/bin/python3 /home/username/autoupdateriot/autoupdateriot.py



