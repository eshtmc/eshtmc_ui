FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requestment.txt /

RUN yum -y install epel-release && yum update -y && yum -y install python-virtualenv python-pip && pip install --upgrade pip && pip install -r requestment.txt

COPY . /eshtmc_ui

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application