from flask import render_template, request

from . import main
from .forms import PaymentForm
from .piastrix import Piastrix


@main.route('/', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    piastrix = Piastrix()
    if request.method == 'POST':
        if form.validate_on_submit():
            amount = request.form.get('amount')
            currency = request.form.get('currency')
            description = request.form.get('description')
            shop_order_id = request.form.get('shop_order_id', '123456')
            if currency == '978':
                return piastrix.pay(amount, currency, description, shop_order_id)
            elif currency == '840':
                return piastrix.bill(amount, currency, description, shop_order_id)
            elif currency == '643':
                return piastrix.invoice(amount, currency, description, shop_order_id)

    return render_template('payment.html', title='Оплата', form=form)
