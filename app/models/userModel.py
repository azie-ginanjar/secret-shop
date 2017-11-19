from app.dao import daoPool
from flask_restplus import fields

db = daoPool.sqlDAO


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), nullable=True, unique=True)

    def __init__(self, username, email, password, address):
        self.username = username
        self.email = email
        self.address = address
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


# Model definition
class ApiModel:
    def __init__(self, api):
        self.userModel = api.model('userModel', {
            "id": fields.Integer,
            "username": fields.String,
            "email": fields.String,
            "address": fields.String,
            "password": fields.String
        })

        self.usersModel = api.model('usersModel', {
            "users": fields.List(fields.Nested(self.userModel))
        })

        self.postModel = api.model('postModel', {
            "success": fields.Boolean
        })

        self.fieldModel = api.model('fieldModel', {
            "field": fields.String
        })

        self.paraErrorModel = api.model('paraErrorModel', {
            "error": fields.Nested(self.fieldModel),
            "message": fields.String
        })
