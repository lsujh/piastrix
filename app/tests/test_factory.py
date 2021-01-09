import hashlib
from flask import request

from app import create_app, db
from main.forms import PaymentForm
from main.models import Payment
from config import TestConfig
from main.piastrix import piastrix, sign_


def test_app_creates(app):
    assert app


def test_config():
    assert not create_app().testing


def test_payment(client):
    response = client.get('/')
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert '<title>Оплата</title>' in html


def test_payment_post(client):
    data = {'amount': 150, 'currency': '840', 'description': 'test payment'}
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert 'test payment'.encode() in response.data


def test_piastrix_pay(client, app):
    with app.test_request_context('/'):
        data = {'amount': 150, 'currency': '978', 'description': 'test payment'}
        response = client.post('/', data=data)
        data['shop_order_id'] = '195'
        pay = piastrix(**data)
        assert 'https://pay.piastrix.com/ru/pay' in pay


def test_piastrix_bill(client):
    data = {'amount': 150, 'currency': '840', 'description': 'test payment'}
    response = client.post('/', data=data)
    data['shop_order_id'] = '195'
    pay = piastrix(**data)
    assert b'https://wallet.piastrix.com/ru/bill/pay/' in pay.response[0]
    assert pay.status_code == 302


def test_piastrix_invoice(client, app):
    with app.test_request_context('/'):
        data = {'amount': 150, 'currency': '643', 'description': 'test payment'}
        response = client.post('/', data=data)
        data['shop_order_id'] = '195'
        pay = piastrix(**data)
        assert 'https://pay.piastrix.com/result/ps/advcash' in pay


def test_post_model(app, client):
    payment = Payment(amount=150, currency='840', description='test', shop_id=5, shop_order_id='123456')
    db.session.add(payment)
    db.session.commit()
    assert payment.id > 0
    assert payment.__repr__() == '123456'


def test_piastrixs_sign(client):
    data = dict(amount=333, currency='840', shop_id=TestConfig.SHOP_ID,
                shop_order_id='987', payway=TestConfig.PAY_WAY)
    my_hash = sign_(**data)
    assert my_hash == hashlib.sha256('333:840:advcash_rub:5:987SecretKey01'.
                                     encode('utf-8')).hexdigest()


def test_not_submitted(app):
    with app.test_request_context(method='GET', data={}):
        f = PaymentForm(request.form, csrf_enabled=False)
        assert not f.is_submitted()
        assert not f.validate_on_submit()


def test_submitted_not_valid(app):
    with app.test_request_context(method='POST', data={}):
        f = PaymentForm(request.form, csrf_enabled=False)
        assert f.is_submitted()
        assert not f.validate()


def test_submitted_and_valid(app):
    data = {'amount': 150, 'currency': '978', 'description': 'test payment'}
    with app.test_request_context(method='POST', data=data):
        f = PaymentForm(request.form, csrf_enabled=False)
        assert f.data.get('description') == 'test payment'
        assert f.validate_on_submit()
