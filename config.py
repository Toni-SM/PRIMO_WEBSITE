import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "files"
    ALLOWED_EXTENSIONS = set(['pdf'])

class ProductionConfig(Config):
    # TODO: generate SECRET_KEY with python -c "import os; print(str(os.urandom(16)))"
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') or \
        'sqlite:///' + os.path.join(_basedir, 'PRIMO-DB.db3')

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'devkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(_basedir, 'PRIMO-DB.db3')

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'testkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(_basedir, 'PRIMO-DB.db3')


# custom configuration
config = DevelopmentConfig

host = '0.0.0.0'
port = 80
