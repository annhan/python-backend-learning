import pika, json

from config import CLOUDAMQP_URL
from print_debug_win import print_debug

params = pika.URLParameters(CLOUDAMQP_URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()


def set_content(type):
    return pika.BasicProperties(
                content_type=type,
                content_encoding='utf-8',
                headers={'key': 'value'},
                delivery_mode = 2,
            )
def publish(method, cmd):
    properties = set_content(method)
    #data = json.dumps(cmd)
    data = cmd
    channel.basic_publish(
        exchange='', 
        routing_key='task_queue11',
        properties=properties,
        body=data)
    #print("[x] Sent message in flask " + str(data))