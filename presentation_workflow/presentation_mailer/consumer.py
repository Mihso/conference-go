import json
from pika.exceptions import AMQPConnectionError
import pika
import django
import os
import time
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue="presentation_approvals")
        channel.queue_declare(queue="presentation_rejections")

        def process_rejection(ch, method, properties, body):
            email = json.loads(body)
            name = email["presenter_name"]
            title = email["title"]
            presenter_em = email["presenter_email"]
            send_mail(
                "Your presentation has been rejected",
                f"{name}, we're happy to tell you that your presentation {title} has been rejected",
                "admin@conference.go",
                [presenter_em],
                fail_silently=False,
            )
            print(email)

        def process_approval(ch, method, properties, body):
            email = json.loads(body)
            name = email["presenter_name"]
            title = email["title"]
            presenter_em = email["presenter_email"]
            send_mail(
                "Your presentation has been approved",
                f"{name}, we're happy to tell you that your presentation {title} has been approved",
                "admin@conference.go",
                [presenter_em],
                fail_silently=False,
            )
            print(email)

        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("could not connect")
        time.sleep(2)

# def process_message(ch, method, properties, body):
#     # email = json.loads(body)
#     # name = email["presenter_name"]
#     # title = email["title"]
#     # presenter_em = email["presenter_email"]
#     # send_mail(
#     #     "Your presentation has been accepted",
#     #     "{name}, we're happy to tell you that your presentation {title} has been accepted",
#     #     "admin@conference.go",
#     #     [presenter_em],
#     #     fail_silently=False,
#     # )
#     # print(email)


# def process_approval():
#     parameters = pika.ConnectionParameters(host="rabbitmq")
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#     channel.queue_declare(queue="presentation_approvals")
#     channel.basic_consume(
#         queue="presentation_approvals",
#         on_message_callback=process_message,
#         auto_ack=True,
#     )
#     channel.start_consuming()


# def process_rejection():
#     parameters = pika.ConnectionParameters(host="rabbitmq")
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#     channel.queue_declare(queue="presentation_rejections")
#     channel.basic_consume(
#         queue="presentation_rejections",
#         on_message_callback=process_message,
#         auto_ack=True,
#     )
#     channel.start_consuming()
