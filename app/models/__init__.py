
def init_model(sqldao):
    from .userModel import User
    from .roleModel import Role
    sqldao.create_all()
