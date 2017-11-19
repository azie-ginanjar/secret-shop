from flask_restplus import Api, Namespace

from .userController import api as ns1

api = Api(version='2.2',
          title='Flask Restful plus Api',
          doc='/api',
          description='Document for Restful api',
          contact='tsungwu@cyber00rn.org',
          default='tweet')

api.add_namespace(ns1, path='/api/user')
