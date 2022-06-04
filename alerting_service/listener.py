from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import alert_handler.alert as alerts
from flask_mail import Mail, Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pika
import time
import json


time.sleep(30)

print("Worker started")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='msg_queue', durable=True)

print("Worker connected")


def callback(ch, method, properties, body):
    cmd = body.decode()
    print("Received %s" % cmd)
    data = json.loads(cmd.replace("\'", "\""))
    print(data)
    try:
        volunteer_email = data['volunteer_email']
        refugee_name = data['refugee_name']
        members_no = data['members_no']

        from_address = ''
        to_address = volunteer_email
        message = MIMEMultipart('Foobar')
        message['Subject'] = 'Booking'
        message['From'] = from_address
        message['To'] = to_address
        text = str(refugee_name) + " booked your accommodation for " + str(members_no) + " people"
        content = MIMEText(text, 'plain')
        message.attach(content)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        f = open("mail_pass", "r")
        password = ''
        mail.login(from_address, password)
        mail.sendmail(from_address,to_address, message.as_string())
        mail.close()
    except Exception as e1:
            print('error is' + e1, flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='msg_queue', on_message_callback=callback)
channel.start_consuming()