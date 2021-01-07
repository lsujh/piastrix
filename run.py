import logging

from app import create_app


app = create_app()
logging.basicConfig(filename='error.log', level=logging.INFO)


if __name__ == '__main__':
    app.run()
