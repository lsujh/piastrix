import os
import tempfile
import pytest

from app import create_app, db
from config import Config

@pytest.fixture
def app():
    return create_app('config.Config')


@pytest.fixture
def client(app):
    db_fd, Config.SQLALCHEMY_DATABASE_URI = tempfile.mkstemp()

    with app.test_client() as client:
        with app.app_context():
           db.init_app(app)
        yield client

    os.close(db_fd)
    os.unlink(Config.SQLALCHEMY_DATABASE_URI)