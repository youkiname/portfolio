from app import create_app
from config import config

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(config.HOST, port=config.PORT)
