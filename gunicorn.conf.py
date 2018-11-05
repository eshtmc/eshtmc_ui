import multiprocessing

bind = "127.0.0.1:8000"
workers = 2
# workers是工作线程数，一般设置成：服务器CPU个数 + 1
# errorlog = '/eshtmc_ui/gunicorn.error.log'
# accesslog = './gunicorn.access.log'
# loglevel = 'debug'
proc_name = 'eshtmc_ui'