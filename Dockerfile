FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requestment.txt /

RUN yum update && yum -y install epel-release zlib-devel bzip2-devel openssl-devel ncurses-devel\
 sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel python-virtualenv python-pip \
 && pip install -i http://mirrors.aliyun.com/pypi/simple/ -r requestment.txt

COPY . /eshtmc_ui

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application