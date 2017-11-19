import logging
import os
from flask import Flask
from app.util.hashUtil import toSHA256


CONFIG_NAME_MAPPER = {
    'development': 'config.Development.cfg',
    'testing': 'config.Testing.cfg',
    'production': 'config.Production.cfg'
}


def create_app(flask_config_name=None):
    '''' create flask app '''

    ## Load Config
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'development'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name

    try:
        if CONFIG_NAME_MAPPER[flask_config_name] is None:
            return None
    except KeyError:
        return None

    ## Creat app
    app = Flask(__name__)
    app.config.from_pyfile(CONFIG_NAME_MAPPER[flask_config_name])
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

    ## Set logger
    logging.basicConfig(format=app.config['LOGGER_FORMAT'], level=app.config['LOGGER_LEVEL'])

    ## db init
    from app.dao import daoPool
    daoPool.init_app(app)

    from app.models.userModel import User

    # me = User('admin', 'admin@example.com', toSHA256("admin"), "Jl. ABC no. 123")
    # daoPool.sqlDAO.session.add(me)
    # daoPool.sqlDAO.session.commit()

    ## Oauth init
    # from app import oauth
    # oauth.init_oauth(app)


    ## Api init
    from app.controllers import api

    api.init_app(app)

    return app
