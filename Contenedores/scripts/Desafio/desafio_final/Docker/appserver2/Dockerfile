FROM django
RUN apt-get update && apt-get install -y python-pip cron
RUN pip install uwsgi python-dateutil requests
ADD appserver2 /appserver2
ADD entry_point.sh /entry_point.sh
RUN chmod a+x entry_point.sh
CMD ./entry_point.sh
