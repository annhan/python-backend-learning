from flask import Flask
import pika
import os,sys,datetime,time
from dotenv import load_dotenv
from threading import Thread
load_dotenv()


app = Flask(__name__)


def print_debug(*msg):
    print(datetime.datetime.now().strftime("%H:%M:%S"), "|" , *msg, flush=True)
    sys.stdout.flush()

def callback(ch, method, properties, body):
    cmd = body.decode()
    
    if properties.content_type == 'product_created':
        print_debug("product created in DATABASE",cmd)
    elif properties.content_type == 'product_updated':
        print_debug("product updated in DATABASE",cmd)
    elif properties.content_type == 'product_deleted':
        print_debug("product deleted in DATABASE",cmd)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


def thread_listerning():
    #return
    connection = pika_connect()
    channel = connection.channel()
    channel.queue_declare(queue='task_queue11', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue11', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    connection.close()


@app.route('/')
def index():
    return 'OK'


@app.route('/add-job/<cmd>')
def add(cmd):
    return " [x] Sent: %s" % cmd


def pika_connect():
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    return connection

def pika_close(conec):
    conec.close()

def set_content(type):
    return pika.BasicProperties(
                content_type=type,
                content_encoding='utf-8',
                headers={'key': 'value'},
                delivery_mode = 2,
            )

def send_cmd(conec,cmd):
    channel = conec.channel()
    channel.queue_declare(queue='task_queue11', durable=True)
    prop = set_content('product_created')
    channel.basic_publish(
        exchange='',
        routing_key='task_queue11',
        body=cmd,
        properties=prop)
    print_debug(" pub finish")

if __name__ == '__main__':
    connection = pika_connect()
    function = thread_listerning
    t1=Thread(target=function)
    t1.daemon = True
    t1.start()
    i = 0
    send_cmd(connection,cmd = str(i))
    while(True):
        i=i+1
        if i<10:
            #pass
            send_cmd(connection,cmd = str(i))
        elif i ==10:
            print_debug("done pub XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            pika_close(connection)

    #app.run(debug=True, host='0.0.0.0')