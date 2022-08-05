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




def thread_listerning():
    print_debug(' [*] Connecting to server ...')
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    print_debug(url)
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue11', durable=True)

    print_debug(' [*] Waiting for messages.')


    def callback(ch, method, properties, body):
        print_debug(" [x] Received %s" % body)
        cmd = body.decode()

        if cmd == 'hey':
            print_debug("hey there")
        elif cmd == 'hello':
            print_debug("well hello there")
        else:
            print_debug("sorry i did not understand ", cmd)

        print_debug(" [x] Done")

        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue11', on_message_callback=callback)
    channel.start_consuming()






@app.route('/')
def index():
    return 'OK'


@app.route('/add-job/<cmd>')
def add(cmd):
    
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    print_debug(url)
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return " [x] Sent: %s" % cmd

def test(cmd):
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue11',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()

if __name__ == '__main__':

    function = thread_listerning
    t1=Thread(target=function)
    t1.daemon = True
    t1.start()
    test("gfgfgfgf")
    i = 0
    while(True):
        time.sleep(1)
        i=i+1
        test(str(i))
    #app.run(debug=True, host='0.0.0.0')