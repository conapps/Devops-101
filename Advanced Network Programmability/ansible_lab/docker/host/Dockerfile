# HOST image - used to create containers to be managed by master

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
FROM ansible_base:latest

# copy script from local disk to file system inside Docker image
COPY run.sh /var/

COPY authorized_keys /root/.ssh/authorized_keys

# Generally a good idea to have these, extensions sometimes need them
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# adjust file permissions to make run.sh executable
RUN chmod 755 /var/run.sh
