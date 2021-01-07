import os
import tempfile
import pytest

from app import create_app, db, bootstrap
from config import TestConfig


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        # db.session.remove()
        # db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

#
#
# @pytest.fixture
# def app():
#     return create_app('config.TestConfig')
#
#
# @pytest.fixture
# def client(app):
#     db_fd, TestConfig.SQLALCHEMY_DATABASE_URI = tempfile.mkstemp()
#     with app.test_client() as client:
#         with app.app_context():
#            db.init_app(app)
#         yield client
#     os.close(db_fd)
#     os.unlink(TestConfig.SQLALCHEMY_DATABASE_URI)

# @pytest.fixture
# def app():
#     app = create_app('config.TestConfig')
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


# DB_URI = 'sqlite://'  # SQLite :memory: database

# @pytest.fixture(scope='function')
# def db(app, client):
#
#     db.create_all()
#     yield db
#     db.drop_all()

# @pytest.fixture
# def session(app):
#     connection = db.engine.connect()
#     transaction = connection.begin()
#     #options = dict(bind=connection, binds={})
#     options = dict(bind=connection)
#     session = db.create_scoped_session(options=options)
#     yield session
#     # Finalize test here
#     transaction.rollback()
#     connection.close()
#     session.remove()