import os

from app import create_app
# from main.models import Payment

def test_app_creates(app):
    assert app

def test_config():
    assert not create_app(os.getenv('FLASK_ENV', 'config.Config')).testing

def test_payment(client):
    response = client.get('/')
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert '<title>Оплата</title>' in html


def test_payment_post(client):
    data = {'amount': 150, 'currency': '840', 'description': 'test', 'shop_id': 5,}
    response = client.post('/', data=data)
    assert 'test'.encode() in response.data


# def test_post_model(session):
#     post = Payment(amount=150, currency='840', description='test', shop_id=5, shop_order_id='123456')
#     session.add(post)
#     session.commit()
#     assert post.id > 0