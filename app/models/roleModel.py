from flask_restplus import fields

from app.dao import daoPool

db = daoPool.sqlDAO


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Id %r>' % self.name

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    @classmethod
    def find_role_by_id(cls, id):
        query = cls.query
        query = query.filter(cls.id == id)
        return query.first()


# Model definition
class ApiModel:
    def __init__(self, api):
        self.roleModel = api.model('roleModel', {
            "id": fields.Integer,
            "name": fields.String
        })

        self.rolesModel = api.model('roleModel', {
            "roles": fields.List(fields.Nested(self.roleModel))
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
