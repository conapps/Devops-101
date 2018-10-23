FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
ADD requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
