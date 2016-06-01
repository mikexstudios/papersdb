# Pull base image.
FROM ubuntu:14.04

RUN apt-get update && \
    apt-get install -y vim-tiny screen wget

# Installs python 2.7.6 and packages necessary to install requirements.txt
RUN apt-get install -y python python-dev python-pip git

# Set up our app files and install
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
# Since pip -e are installed in /usr/src/app/src, it gets overwritten if we
# mount the current directory in /usr/src/app. Thus, we install src packages
# in another directory. See: http://stackoverflow.com/q/29905909/66771
RUN pip install -r requirements.txt --src /usr/local/src

# app
EXPOSE 80
VOLUME ["/usr/src/app"]
CMD python manage.py syncdb --noinput && \
    python manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell && \
    python manage.py runserver 0.0.0.0:80
