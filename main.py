from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.inspection import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://olawale@localhost:5432/alchemy'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    addresses = db.relationship('Address')

    def serialize(self):
        return Serializer.serialize(self)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return Serializer.serialize(self)

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

@app.route("/")
def home():
    return jsonify({ "Response": True })

@app.route("/get_address")
def get_address():
    address = Address.query.all()
    return jsonify(address[1].serialize())

@app.route("/get_user")
def get_user():
    user = User.query.all()
    # print(user[0].addresses[0].serialize())
    print(user[0].addresses[1].serialize())
    return jsonify({ "Success": False })

@app.route("/create_user")
def create_user():
    # user = User(username="brainyfarm")
    user = User(username="brainyfarm")
    db.session.add(user)
    db.session.commit()
    db.session.close()

@app.route("/create_address")
def create_adress():
    address = Address(address="15 Alh Lukman", user_id=1)
    db.session.add(address)
    db.session.commit()
    db.session.close()

    return jsonify({ "Success": True })
    