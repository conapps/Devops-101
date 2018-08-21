FROM django
RUN apt-get update && apt-get install -y python-pip cron
RUN pip install uwsgi python-dateutil requests
ADD appserver1 /appserver1
ADD entry_point.sh /entry_point.sh
RUN chmod a+x entry_point.sh
CMD ./entry_point.sh
