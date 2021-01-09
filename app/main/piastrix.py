import json
import hashlib
from urllib.request import Request, urlopen
from flask import render_template, redirect, flash, url_for

from app import db
from .models import Payment
from config import Config


def piastrix(amount, currency, description, shop_order_id):
    if currency == '978':
        sign = sign_(amount=amount, currency=currency, shop_id=Config.SHOP_ID, shop_order_id=shop_order_id)
        form = {
            'url': 'https://pay.piastrix.com/ru/pay',
            'name': 'Pay',
            'amount': amount,
            'currency': currency,
            'description': description,
            'shop_id': Config.SHOP_ID,
            'shop_order_id': shop_order_id,
            'sign': sign,
        }
        save(amount, currency, description, Config.SHOP_ID, shop_order_id)
        return render_template('pay.html', form=form)

    elif currency == '840':
        sign = sign_(shop_amount=amount, shop_currency=currency, shop_id=Config.SHOP_ID,
                     shop_order_id=shop_order_id, payer_currency=currency)
        data = {
            'payer_currency': currency,
            'shop_amount': amount,
            'shop_currency': currency,
            'shop_id': Config.SHOP_ID,
            'shop_order_id': shop_order_id,
            'sign': sign,
            'description': description,
        }
        req = Request('https://core.piastrix.com/bill/create', json.dumps(data).encode('utf-8'),
                      headers={'Content-Type': 'application/json'}, method='POST')
        return pay_bill_invoice(req, amount, currency, description, shop_order_id)

    elif currency == '643':
        sign = sign_(amount=amount, currency=currency, shop_id=Config.SHOP_ID,
                     shop_order_id=shop_order_id, payway=Config.PAY_WAY)
        data = {
            'amount': amount,
            'currency': currency,
            'shop_id': Config.SHOP_ID,
            'shop_order_id': shop_order_id,
            'description': description,
            'payway': Config.PAY_WAY,
            'sign': sign
        }
        req = Request('https://core.piastrix.com/invoice/create', json.dumps(data).encode('utf-8'),
                      headers={'Content-Type': 'application/json'}, method='POST')
        return pay_bill_invoice(req, amount, currency, description, shop_order_id)


def pay_bill_invoice(req, amount, currency, description, shop_order_id):
    with urlopen(req) as response:
        data = json.loads(response.read())
        if data['result']:
            if currency == '643':
                form = data['data']
                save(amount, currency, description, Config.SHOP_ID, shop_order_id)
                return render_template('invoice.html', form=form)
            elif currency == '840':
                data = data['data']
                save(amount, currency, description, Config.SHOP_ID, shop_order_id)
                return redirect(data['url'])
        else:
            flash(f'Ошибка. Пожалуйста, попробуйте еще раз: {data["message"]}')
            return redirect(url_for('main:payment'))


def sign_(**kwargs):
    data = [str(kwargs[key]) for key in sorted(kwargs.keys())]
    hex_hash = hashlib.sha256((':'.join(data) + Config.SECRET_KEY).encode('utf-8')).hexdigest()
    return hex_hash


def save(*args):
    payment = Payment(*args)
    db.session.add(payment)
    db.session.commit()
