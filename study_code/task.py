# -*- coding: utf-8 -*-

from celery import Celery

# app = Celery('task', broker='redis://localhost/0',
#                    backend='redis://localhost/0')
# app = Celery('tasks', broker='amqp://guest@localhost//')
app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task
def add(x, y):

    return x+y



print "hahahhahaahhh"


# if __name__ == '__main__':
#     result = add.delay(30, 42)