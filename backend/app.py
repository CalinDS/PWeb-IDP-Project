import multiprocessing
import os
from webbrowser import get
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import api.routes.user_route as users
import api.routes.accommodation_route as accommodations
import api.routes.booking_route as bookings
from infrastrucure.db_config import config_db_for_app, db
import pika
from prometheus_client import REGISTRY, CollectorRegistry, start_http_server
from prometheus_client import Counter, Gauge, Summary, Histogram, Info
from multiprocessing.pool import ThreadPool
from core.model.accommodation_model import AccommodationModel
from core.model.booking_model import BookingModel
from core.model.user_model import UserModel
import time



# pool = ThreadPool(1)
# pool.apply_async(start_http_server, (8005, ))

c = Counter('users_get_call_counter', 'Counter that tracks get calls on the /users API path')
g = Gauge('accommodation_gauge',
        'Gauge that tracks the number of accomodations made or deleted by the system')
i = Info('project_info', 'Project info')
i.info({'version': '1.0.1', 'buildhost': 'dragoss.calin@gmail.com'})

app = Flask(__name__)
CORS(app)
app = config_db_for_app(app)
app.register_blueprint(users.users_api)
app.register_blueprint(accommodations.accommodations_api)
app.register_blueprint(bookings.bookings_api)

@app.route('/users', methods = ['GET'])
def retrieve_users():
    c.inc()
    users = UserModel.query.all()
    return str(users), 200


@app.route('/users/<string:auth_id>', methods = ['GET'])
def retrieve_user_by_auth_id(auth_id):
    print(c, flush=True)
    print("userauth", flush=True)
    c.inc()
    print(c._value.get(), flush=True)
    user = UserModel.query.filter_by(auth_id=auth_id).first()
    if user:
        resp = {
            "id": user.id,
            "auth_id": user.auth_id,
            "email": user.email,
            "name": user.name,
            "type": user.type,
            "contact_info": user.contact_info,
            "family_members_no": user.family_members_no
        }
        if user.type == 'refugee':
            booking = BookingModel.query.filter_by(refugee_id=user.id).first()
            if booking:
                accommodation = AccommodationModel.query.filter_by(id=booking.accommodation_id).first()
                owner = UserModel.query.filter_by(id=accommodation.owner_id).first()
                resp["accommodation"]= {
                    "address": accommodation.address,
                    "photo": accommodation.photo,
                    "owner_name": owner.name,
                    "contact_info": owner.contact_info,
                    "booking_id": booking.id
                }
        return jsonify(resp), 200
    return f"User with auth_id={auth_id} doesn't exist", 404

@app.route('/accommodations/create', methods = ['POST'])
def create_accommodation():
    g.inc()
    print(g, flush=True)
    print(str(g._value.get()), flush=True)
    print("gauging", flush=True)
    data = request.get_json()
    try:
        accommodation = AccommodationModel(
            owner_id=data["owner_id"],
            photo=data["photo"],
            beds_no=data["beds_no"],
            address=data["address"]
            )
        db.session.add(accommodation)
        db.session.commit()
        return "Accommodation added", 200
    except Exception as e:
        print(e)
        return "Error", 404

@app.route('/accommodations/<int:id>/delete', methods=['GET','POST', 'PUT', 'DELETE'])
def delete_accommodation(id):
    g.dec()
    print(g, flush=True)
    print(str(g._value.get()), flush=True)
    print("gauging", flush=True)
    accommodation = AccommodationModel.query.filter_by(id=id).first()
    if accommodation:
        bookings = BookingModel.query.filter_by(accommodation_id=accommodation.id).all()
        for b in bookings:
            db.session.delete(b)
        db.session.delete(accommodation)
        db.session.commit()
        return "Deleted", 200
    return f"User with id={id} doesn't exist", 404


if __name__ == "__main__":
    start_http_server(8005)
    app.run(host="0.0.0.0")

