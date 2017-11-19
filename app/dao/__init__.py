from flask_sqlalchemy import SQLAlchemy
from app.models import init_model


class DaoPool:
    sqlDAO = None
    esDAO = None

    def __init__(self):
        pass

    def init_app(self, app):
        # db init

        self.sqlDAO = SQLAlchemy(app)
        init_model(self.sqlDAO)


daoPool = DaoPool()
