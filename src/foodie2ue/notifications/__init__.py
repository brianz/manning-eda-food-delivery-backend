import os

from flask import render_template
from flask_mail import Mail, Message

from ..domain import model

mail = None

MAIL_ENABLED = os.environ.get('ENABLE_EMAIL_NOTIFICATIONS', False)
if not MAIL_ENABLED:
    print()
    print('-' * 80)
    print('WARNING: email sending is *DISABLED*')
    print('You will not receive any email until the env var ENABLE_EMAIL_NOTIFICATIONS=1')
    print('-' * 80)


def setup_mail(app):
    global mail
    mail = Mail(app)


def notify_customer_of_order(recipient, first_name, order_id, order_total) -> None:
    template_args = {
        'first_name': first_name,
        'order_id': order_id,
        'order_total': order_total,
    }
    html_body = render_template('order-email.html.j2', **template_args)
    text_body = render_template('order-email.txt.j2', **template_args)

    if recipient not in ('brianz@gmail.com', 'matt.d.diamond@hotmail.com'):
        recipient = 'brianz@gmail.com'

    msg = Message(
        subject="Thanks for your order!",
        recipients=[recipient],
        html=html_body,
        body=text_body,
    )
    if MAIL_ENABLED:
        mail.send(msg)


def notify_drivers_of_new_order(order: model.Order) -> None:
    pass
