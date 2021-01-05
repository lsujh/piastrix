import os
import logging

from app import create_app


app = create_app(os.getenv('FLASK_ENV', 'config.Config'))
logging.basicConfig(filename='error.log', level=logging.INFO)


if __name__ == '__main__':
    app.run()
