from distutils.log import error
import json
from flask import request, Blueprint, jsonify
from infrastrucure.db_config import db
from core.model.booking_model import BookingModel
from core.model.accommodation_model import AccommodationModel
from core.model.user_model import UserModel
import requests as req
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

bookings_api = Blueprint('bookings_api', __name__)


@bookings_api.route('/bookings/create', methods = ['POST'])
def create_booking():
    data = request.get_json()
    print(data)
    refugee = UserModel.query.filter_by(id=data["refugee_id"]).first()
    members_no = refugee.family_members_no
    refugee_name = refugee.name
    accomm = AccommodationModel.query.filter_by(id=data["accommodation_id"]).first()
    volunteer_id = accomm.owner_id
    volunteer = UserModel.query.filter_by(id=volunteer_id).first()
    volunteer_email = volunteer.email
    try:
        booking = BookingModel(
                refugee_id=data["refugee_id"],
                accommodation_id=data["accommodation_id"]
            )
        db.session.add(booking)
        db.session.commit()

        content = {
            "volunteer_email": volunteer_email,
            "refugee_name": refugee_name,
            "members_no": members_no
        }
        print(content)

        # session = req.Session()
        # retry = Retry(connect=3, backoff_factor=1)
        # adapter = HTTPAdapter(max_retries=retry)
        # session.mount('http://', adapter)
        # session.mount('https://', adapter)
        # page = ''
        # try:
        #     page = session.post("http://alert:6000/alerts", json=content, timeout=10)
        # except Exception as e1:
        #     print(e1)

        resp = req.post("http://127.0.0.1:6000/alerts", json=content)

        return "Booking added", 200
    except Exception as e:
        print(e)
        return "Error", 404




#retrieve
@bookings_api.route('/bookings', methods = ['GET'])
def retrieve_bookings():
    bookings = BookingModel.query.all()
    return str(bookings), 200

#retrieve
@bookings_api.route('/bookings/<int:id>', methods = ['GET'])
def retrieve_volunteer_bookings(id):
    accommodations = AccommodationModel.query.filter_by(owner_id=id).all()
    bookings_by_accommodation = []
    for a in accommodations:
        bookings = BookingModel.query.filter_by(accommodation_id=a.id).all()
        if len(bookings) == 0:
            continue
        refugees = []
        for b in bookings:
            ref = UserModel.query.filter_by(id=b.refugee_id).first()
            refugees.append({
                "refugee_name": ref.name,
                "family_members_no": ref.family_members_no,
                "contact_info": ref.contact_info,
                "booking_id": b.id
            })
        bookings_by_accommodation.append({
            "accommodation":  {
                "address": a.address,
                "photo": a.photo,
                "beds_no": a.beds_no
            },
            "refugees": refugees
        })

    return jsonify(bookings_by_accommodation), 200


#update
@bookings_api.route('/bookings/<int:id>/update', methods = ['PUT'])
def update_booking(id):
    booking = BookingModel.query.filter_by(id=id).first()
    data = request.get_json()
    if booking:
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return json.loads(str(booking)), 200
    return f"Accomodation with id={id} doesn't exist", 404


#delete
@bookings_api.route('/bookings/<int:id>/delete', methods=['GET','POST', 'PUT', 'DELETE'])
def delete_booking(id):
    booking = BookingModel.query.filter_by(id=id).first()
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return "Deleted", 200
    return f"User with id={id} doesn't exist", 404