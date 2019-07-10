# -*- coding: utf-8 -*-

from celery import Celery

app = Celery('task', broker='redis://localhost/0',
                     backend='redis://localhost/0')

@app.task
def add(x, y):
    print ("running.......... ", x, y)
    return x+y


if __name__ == '__main__':
    result = add.delay(30, 42)