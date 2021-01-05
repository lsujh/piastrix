from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField, TextAreaField


class PaymentForm(FlaskForm):
    CURRENCY = [(978, 'EUR'), (840, 'USD'), (643, 'RUB')]
    amount = DecimalField('Сумма оплаты')
    currency = SelectField('Валюта оплаты', choices=CURRENCY)
    description = TextAreaField('Описание товара')
    submit = SubmitField('Оплатить')
