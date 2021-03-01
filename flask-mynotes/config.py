class Configuration:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    DEBUG = False
    DB_NAME = "app.db"


class DevConfiguration(Configuration):
    DEBUG = True
    TESTING = True
    HOST = 'localhost'
    PORT = 9090


config = DevConfiguration()
