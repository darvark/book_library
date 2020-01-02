FROM centos:latest

# Expose default port for hosting app
EXPOSE 5000

# Install requirements
RUN yum update -y && yum install -y \
    python3 \
    python3-pip &&\
    pip3 install flask sqlalchemy

# Create directory for source code and database
RUN mkdir -p /var/www/app

# Create volume for app source code and database
VOLUME /var/www/app

# Copy source code
COPY app/ /var/www/app

ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
