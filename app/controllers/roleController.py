from flask_restplus import reqparse, Resource, Namespace
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from app.dao import daoPool
from app.models.roleModel import Role as RoleModel, ApiModel

api = Namespace('roles', description='role operation')
apiModel = ApiModel(api)
sqlDAO = daoPool.sqlDAO

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='role name', location='json')


@api.route('')
class Users(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get List of roles . \n\n ')
    @api.response(200, 'Success', apiModel.rolesModel)
    def get(self):
        """ Get all roles """
        result = {}
        roles = []

        resp = RoleModel.query.all()
        if resp is None:
            return []

        for x in resp:
            roles.append(x.to_dict())
        result['roles'] = roles
        return result

    @api.expect(parser, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Add new role . \n\n ')
    def post(self):
        """ add user """
        args = parser.parse_args()

        role = RoleModel(args['name'])
        try:
            sqlDAO.session.add(role)
            sqlDAO.session.commit()
        except IntegrityError:
            raise InternalServerError("role name already in used")

        return role.to_dict()