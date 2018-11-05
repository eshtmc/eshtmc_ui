FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requirement.txt /

RUN yum -y install epel-release && yum update -y && yum -y install python-virtualenv python34-pip && pip3 install -r requirement.txt

COPY . /eshtmc_ui
WORKDIR /eshtmc_ui

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application