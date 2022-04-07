# MASTER image - used to create the master container to manage hosts

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
FROM ansible_base:latest

RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y software-properties-common
RUN apt-add-repository ppa:ansible/ansible
RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y ansible git tmux
RUN apt-get install --no-install-recommends --no-install-suggests -y pip
RUN pip install paramiko

# Generally a good idea to have these, extensions sometimes need them
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Set environment
ADD .vimrc /root/.vimrc
ADD .nanorc /root/.nanorc

# Allow ssh connection for root with password 
RUN echo 'root:Ansible-101' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config

# Allow ssh connection for root with ssh-key 
ADD authorized_keys /root/.ssh/authorized_keys
RUN chown root /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

# Allow ssh connection to hosts with ssh-key directly
COPY ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config

# Copy ssh-key file to allow ssh direct login to router hub
COPY devops101-labs.pem /root/.ssh/devops101-labs.pem
RUN chmod 600 /root/.ssh/devops101-labs.pem

# Install Cisco IOS Ansible Collection
RUN ansible-galaxy collection install cisco.ios

# Change default working directory when login
WORKDIR /root/ansible
RUN echo "cd /root/ansible" >> ~/.profile

CMD ["/usr/sbin/sshd","-D"]

# generate RSA key pair to allow master to communicate with managed nodes
# default private key passphrase is '12345'
# RUN ssh-keygen -t rsa -N 12345 -C "master key" -f master_key
