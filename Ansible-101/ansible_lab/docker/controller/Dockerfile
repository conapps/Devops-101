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
RUN echo 'root:Ansible-101' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
# RUN service ssh start
# EXPOSE 22

# Add ubuntu user to container and configure as default
# RUN useradd -m ubuntu
# RUN echo 'ubuntu:Ansible-101' | chpasswd
# RUN mkdir -p /home/ubuntu/.ssh
# ADD .vimrc /home/ubuntu/.vimrc
# ADD .nanorc /home/ubuntu/.nanorc
# RUN chown -R ubuntu /home/ubuntu
# change working directory
# RUN echo "cd /home/ubuntu/ansible" >> /home/ubuntu/.profile

WORKDIR /root/ansible
RUN echo "cd /root/ansible" >> ~/.profile

CMD ["/usr/sbin/sshd","-D"]

# generate RSA key pair to allow master to communicate with managed nodes
# default private key passphrase is '12345'
# RUN ssh-keygen -t rsa -N 12345 -C "master key" -f master_key
