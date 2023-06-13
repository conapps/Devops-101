# HOST image - used to create containers to be managed by master

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
FROM ansible_base:latest
# FROM ansible101-base:latest

# copy files from local disk to file system inside Docker image
COPY run.sh /var/
COPY authorized_keys /root/.ssh/authorized_keys
COPY ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/config

# Generally a good idea to have these, extensions sometimes need them
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# adjust file permissions to make run.sh executable
RUN chmod 755 /var/run.sh
CMD /var/run.sh
