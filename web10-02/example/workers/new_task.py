#!/usr/bin/env python
import datetime

import pika
import sys
import json
import random

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='test_works', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='test_works', queue='task_queue')

count = 0

while True:
    count += 1
    if count > 100:
        break

    message = {
        "id": count,
        "foo": random.randint(1, 2000)
    }

    channel.basic_publish(
        exchange='test_works',
        routing_key='task_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(" [x] Sent %r" % message)

connection.close()
