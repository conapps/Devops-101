# BASE image - used as a starting point by MASTER and HOST images

FROM ubuntu:22.04

# install required packages
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Montevideo apt-get -y install tzdata
RUN apt-get install -y ansible python3 python3-pip iputils-ping net-tools sudo vim glibc-source
RUN apt-get install --no-install-recommends --no-install-suggests -y \
  aptitude iputils-ping curl ca-certificates man openssh-server locales nano \
  && rm -rf /var/lib/apt/lists/*

# ensure that required directories are created
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

# Add some aliases
ADD .bashrc /root/.bashrc
