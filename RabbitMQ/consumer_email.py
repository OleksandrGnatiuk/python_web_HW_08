import pika

from producer import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='send_email', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_email(email):
    print(f"Message for email:{email} was sent")


def callback(ch, method, properties, body):
    object_id = body.decode()
    contact = Contact.objects(id=object_id)[0]
    # print(contact)
    email = contact.email

    print(f" [x] Received task for sending e-mail for {contact.fullname}")
    send_email(email)
    contact.is_sent = True
    contact.save()
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='send_email', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()