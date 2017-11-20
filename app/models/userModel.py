from app.dao import daoPool
from flask_restplus import fields

db = daoPool.sqlDAO


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role_id = db.Column(db.Integer, nullable=False)

    def __init__(self, username, email, password, address, role_id):
        self.username = username
        self.email = email
        self.address = address
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    @classmethod
    def find_user_by_username_password(cls, username, password):
        query = cls.query
        query = query.filter(cls.username == username)
        query = query.filter(cls.password == password)
        return query.first()


# Model definition
class ApiModel:
    def __init__(self, api):
        self.userModel = api.model('userModel', {
            "id": fields.Integer,
            "username": fields.String,
            "email": fields.String,
            "address": fields.String,
            "password": fields.String,
            "role_id": fields.Integer
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
