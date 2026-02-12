class Config(object):
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Dani016*@localhost:3306/bdidgs801"
    SQLALCHEMY_TRACK_MODIFICATION = False
