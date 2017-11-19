
def init_model(sqldao):
    from .userModel import User
    sqldao.create_all()
