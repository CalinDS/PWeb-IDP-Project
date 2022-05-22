from distutils.log import error
import json
from flask import request, Blueprint
from flask_mail import Mail, Message

alerts_api = Blueprint('alerts_api', __name__)

#create
@alerts_api.route('/alerts', methods = ['POST'])
def receive_alert():
    data = request.get_json()
    print(data)
    volunteer_email = data['volunteer_email']
    refugee_name = data['refugee_name']
    members_no = data['members_no']
    msg = Message(
                'Hello',
                sender ='dragos.plete@gmail.com',
                recipients = [volunteer_email]
                )
    msg.body = str(refugee_name) + " booked your accommodation for " + str(members_no) + " people"
    Mail.send(msg)
    return "success", 200
