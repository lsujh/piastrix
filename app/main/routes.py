from flask import render_template, request

from . import main
from .forms import PaymentForm
from .piastrix import piastrix


@main.route('/', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            amount = request.form.get('amount')
            currency = request.form.get('currency')
            description = request.form.get('description')
            shop_order_id = request.form.get('shop_order_id', '123456')
            return piastrix(amount, currency, description, shop_order_id)

    return render_template('payment.html', title='Оплата', form=form)
