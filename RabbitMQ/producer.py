import pika
from random import randint
from faker import Faker
from mongoengine import connect, StringField, Document, BooleanField

fake = Faker('uk-UA')

connect(host="mongodb+srv://userweb10:567234@cluster0.oqyfihy.mongodb.net/?retryWrites=true&w=majority")

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='inform_contacts', exchange_type='direct')
channel.queue_declare(queue='send_email', durable=True)
channel.queue_bind(exchange='inform_contacts', queue='send_email')


class Contact(Document):
    fullname = StringField(max_length=250, required=True)
    email = StringField(max_length=100, required=True)
    phone = StringField(max_length=20, required=True)
    is_sent = BooleanField(bool=False, required=True)


def main():
    for _ in range(0, randint(10, 15)):
        contact = Contact(
            fullname = fake.name(),
            email = fake.email(),
            phone = fake.phone(),
            is_sent = False
            ).save()
        message = str(contact.id).encode()

        channel.basic_publish(
            exchange='inform_contacts',
            routing_key='send_email',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        contact.is_sent = True
        print(f"E-mail:{contact.email} for contact {contact.fullname} was added to queue")
    connection.close()


if __name__ == '__main__':
    main()
    