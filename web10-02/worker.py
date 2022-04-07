import pika
import time
from db import Contacts
from mail_service import send_email


def callback(ch, method, properties, body):
    _id = body.decode()
    contact = Contacts.objects(id=_id)
    for r in contact:
        email = r.email
        first_name = r.first_name

    send_email('info@my-company.com', email, f"Hello, {first_name}")
    Contacts.objects(id=_id).update_one(set__completed=True)
    time.sleep(1)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='marketing_campaign', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='marketing_campaign', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    main()