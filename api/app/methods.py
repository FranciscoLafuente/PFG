from datetime import datetime
import json
from bson import ObjectId
import pika

host_queue = 'rabbitmq'


def send_to_queue(scan):
    if not scan:
        return
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host_queue))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(scan),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(" [x] Sent MESSAGE")
    connection.close()


def time_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
