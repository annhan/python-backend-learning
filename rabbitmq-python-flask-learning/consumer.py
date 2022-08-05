import pika, json,sys,datetime

from config import CLOUDAMQP_URL
from print_debug_win import print_debug
#from app import Product, db


def callback(ch, method, properties, body):
    cmd = body.decode()
    
    if properties.content_type == 'product_created':
        print_debug("product created in DATABASE",cmd)
    elif properties.content_type == 'product_updated':
        print_debug("product updated in DATABASE",cmd)
    elif properties.content_type == 'product_deleted':
        print_debug("product deleted in DATABASE",cmd)

def consumer():
    params = pika.URLParameters(CLOUDAMQP_URL)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue11', durable=True)
    channel.basic_consume(queue='task_queue11', on_message_callback=callback, auto_ack=True)

    print_debug('[*] Waiting for messages in flask:')
    channel.start_consuming()
    channel.close()