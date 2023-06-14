# BASE image - used as a starting point by MASTER and HOST images

FROM ubuntu:20.04

# install required packages
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Montevideo apt-get -y install tzdata
RUN apt-get install --no-install-recommends --no-install-suggests -y \
  aptitude iputils-ping curl ca-certificates net-tools man vim openssh-server python3 locales nano sudo \
  && rm -rf /var/lib/apt/lists/*

# FROM ubuntu:22.04
# RUN apt-get update
# RUN DEBIAN_FRONTEND=noninteractive TZ=America/Montevideo apt-get -y install tzdata
# RUN apt-get install -y ansible python3 python3-pip iputils-ping net-tools sudo vim
# RUN apt-get upgrade -y
# RUN apt-get install -y apt-utils
# RUN apt-get install -y curl ca-certificates man openssh-server locales nano
# RUN apt-get install -y glibc-source

# ensure that required directories are created
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

# Add some aliases
ADD .bashrc /root/.bashrc
