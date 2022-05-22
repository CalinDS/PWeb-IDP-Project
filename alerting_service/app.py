from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import alert_handler.alert as alerts
from flask_mail import Mail, Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


   
app = Flask(__name__)
CORS(app)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ' ttesttuser12345@gmail.com'
app.config['MAIL_PASSWORD'] = 'Parola1.'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route('/alerts', methods = ['POST'])
def receive_alert():
    data = request.get_json()
    print(data)
    volunteer_email = data['volunteer_email']
    refugee_name = data['refugee_name']
    members_no = data['members_no']

    from_address = 'ttesttuser12345@gmail.com'
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
    password = f.readline()
    mail.login(from_address, password)
    mail.sendmail(from_address,to_address, message.as_string())
    mail.close()
    return "success", 200


app.run(host='0.0.0.0',debug=True,port='6000')