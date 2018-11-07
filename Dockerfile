FROM centos

MAINTAINER Saiun
RUN mkdir eshtmc_ui
ADD ./requirement.txt /

RUN yum -y install epel-release && yum update -y && yum -y install git python-virtualenv python34-pip && pip3 install -r requirement.txt

COPY . /eshtmc_ui
WORKDIR /eshtmc_ui

CMD python3 manage.py migrate

CMD python3 manage.py collectstatic

CMD gunicorn -c gunicorn.conf.py eshtmc_ui.wsgi:application