#!/bin/bash
echo 'Comienzo de script de arranque'
cd /appserver1/ && uwsgi --uwsgi-socket :8000 --module appserver1.wsgi
