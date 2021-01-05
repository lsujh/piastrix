import json
import hashlib
from urllib.request import Request, urlopen
from flask import render_template, redirect, flash, url_for

from app import db
from .models import Payment
from config import Config


class Piastrix:
    def pay(self, amount, currency, description, shop_order_id):
        sign = self._sign(amount=amount, currency=currency, shop_id=Config.SHOP_ID,
                          shop_order_id=shop_order_id)
        form = {
            "url": 'https://pay.piastrix.com/ru/pay',
            "name": 'Pay',
            "amount": amount,
            "currency": currency,
            "description": description,
            "shop_id": Config.SHOP_ID,
            "shop_order_id": shop_order_id,
            "sign": sign,
        }
        self._save(amount, currency, description, Config.SHOP_ID, shop_order_id)
        return render_template('pay.html', form=form)

    def bill(self, amount, currency, description, shop_order_id):
        sign = self._sign(shop_amount=amount, shop_currency=currency, shop_id=Config.SHOP_ID,
                          shop_order_id=shop_order_id, payer_currency=currency)
        data = {
            "payer_currency": currency,
            "shop_amount": amount,
            "shop_currency": currency,
            "shop_id": Config.SHOP_ID,
            "shop_order_id": shop_order_id,
            "sign": sign,
            "description": description,
        }
        request = Request('https://core.piastrix.com/bill/create',
                          json.dumps(data).encode("utf-8"),
                          headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request) as response:
            data = json.loads(response.read())
            if data["result"]:
                data = data["data"]
                self._save(amount, currency, description, Config.SHOP_ID, shop_order_id)
                return redirect(data["url"])
            else:
                flash(f'Ошибка. Пожалуйста, попробуйте еще раз: {data["message"]}')
                return redirect(url_for('payment'))

    def invoice(self, amount, currency, description, shop_order_id):
        sign = self._sign(amount=amount, currency=currency, shop_id=Config.SHOP_ID,
                          shop_order_id=shop_order_id, payway=Config.PAY_WAY)
        data = {
            "amount": amount,
            "currency": currency,
            "shop_id": Config.SHOP_ID,
            "shop_order_id": shop_order_id,
            "description": description,
            "payway": Config.PAY_WAY,
            "sign": sign
        }
        request = Request('https://core.piastrix.com/invoice/create',
                          json.dumps(data).encode("utf-8"),
                          headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request) as response:
            data = json.loads(response.read())
            if data["result"]:
                form = data["data"]
                self._save(amount, currency, description, Config.SHOP_ID, shop_order_id)
                return render_template('invoice.html', form=form)
            else:
                flash(f'Ошибка. Пожалуйста, попробуйте еще раз: {data["message"]}')
                return redirect(url_for('payment'))

    @staticmethod
    def _sign(**kwargs):
        data = [str(kwargs[key]) for key in sorted(kwargs.keys())]
        hex_hash = hashlib.sha256((":".join(data) + Config.SECRET_KEY).encode("utf-8")).hexdigest()
        return hex_hash

    @staticmethod
    def _save(*args):
        payment = Payment(*args)
        db.session.add(payment)
        db.session.commit()
