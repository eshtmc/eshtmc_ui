FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requestment.txt /

RUN yum update && yum -y install epel-release python-virtualenv python-pip && pip install -r requestment.txt -i http://mirrors.aliyun.com/pypi/simple/

COPY . /eshtmc_ui

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application