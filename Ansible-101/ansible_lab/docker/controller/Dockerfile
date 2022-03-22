# MASTER image - used to create the master container to manage hosts

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
FROM ansible_base:latest

RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y software-properties-common
RUN apt-add-repository ppa:ansible/ansible
RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y ansible git tmux

# Generally a good idea to have these, extensions sometimes need them
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD .vimrc /root/.vimrc
ADD .nanorc /root/.nanorc

# COPY authorized_keys /root/.ssh/authorized_keys

# change working directory
WORKDIR /var/ans

# generate RSA key pair to allow master to communicate with managed nodes
# default private key passphrase is '12345'
# RUN ssh-keygen -t rsa -N 12345 -C "master key" -f master_key
