#!/bin/sh

exec uwsgi uwsgi.ini
#exec uwsgi --http-socket 127.0.0.1:3031 --wsgi-file ../foobar.py