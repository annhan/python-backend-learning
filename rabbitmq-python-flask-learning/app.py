from flask import Flask
import pika
import os,sys,datetime,time
from threading import Thread
from config import CLOUDAMQP_URL
from publisher import publish
from consumer import consumer
from print_debug_win import print_debug
app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'


@app.route('/add-job/<cmd>')
def add(cmd):
    return " [x] Sent: %s" % cmd

if __name__ == '__main__':
    function = consumer
    t1=Thread(target=function)
    t1.daemon = True
    t1.start()
    i = 0
    publish('product_created',cmd = str(i))
    while(True):
        i=i+1
        if i<10:
            #pass
            publish('product_created',cmd = str(i))
        elif i ==10:
            print_debug("done pub XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    #app.run(debug=True, host='0.0.0.0')