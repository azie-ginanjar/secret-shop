import os

from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restplus import reqparse, Resource, Namespace
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError, Unauthorized

from app.dao import daoPool
from app.models.userModel import User as UserModel, ApiModel
from ..util.hashUtil import toSHA256

fileDir = os.path.dirname(__file__)

api = Namespace('users', description='user operation')
apiModel = ApiModel(api)
sqlDAO = daoPool.sqlDAO

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='username of user', location='json')
parser.add_argument('email', required=True, help='email of user', location='json')
parser.add_argument('address', required=False, help='address of user', location='json')
parser.add_argument('password', required=True, help='password of user', location='json')

parserLogin = reqparse.RequestParser()
parserLogin.add_argument('username', required=True, help='username of user', location='json')
parserLogin.add_argument('password', required=True, help='password of user', location='json')


@api.route('')
class Users(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get List of users . \n\n ')
    @api.response(200, 'Success', apiModel.usersModel)
    def get(self):
        """ Get all users """
        result = {}
        users = []

        resp = UserModel.query.all()
        if resp is None:
            return []

        for x in resp:
            users.append(x.to_dict())
        result['users'] = users
        return result

    @api.expect(parser, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Add new user by username and email . \n\n ')
    def post(self):
        """ add user """
        args = parser.parse_args()
        user = UserModel(args['username'], args['email'], toSHA256(args["password"]), args["address"])
        try:
            sqlDAO.session.add(user)
            sqlDAO.session.commit()
        except IntegrityError:
            raise InternalServerError("username or email already in used")

        return user


@api.route('/login')
class Login(Resource):
    @api.expect(parser, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='login . \n\n ')
    def post(self):
        args = parserLogin.parse_args()

        resp = UserModel.find_user_by_username_password(args['username'], toSHA256(args["password"]))

        if resp is not None:
            access_token = create_access_token(identity=args['username'])
            return jsonify(access_token=access_token)
        else:
            raise Unauthorized("Bad username or password")
