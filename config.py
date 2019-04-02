
class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "files"
    ALLOWED_EXTENSIONS = set(['pdf'])

class ProductionConfig(Config):
    SECRET_KEY = 'key'
    # TODO: generate SECRET_KEY with python -c "import os; print(str(os.urandom(16)))"

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'devkey'

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'testkey'


# custom configuration
config = DevelopmentConfig

host = '0.0.0.0'
port = 80
