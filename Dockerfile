FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requestment.txt /

RUN yum update -y && yum -y install epel-release python-virtualenv python-pip3

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ -r requestment.txt

COPY . /eshtmc_ui

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application