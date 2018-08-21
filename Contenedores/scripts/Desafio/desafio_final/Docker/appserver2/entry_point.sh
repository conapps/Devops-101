#!/bin/bash
echo 'Comienzo de script de arranque'
cd /appserver2/ && uwsgi --uwsgi-socket :8000 --module appserver2.wsgi
