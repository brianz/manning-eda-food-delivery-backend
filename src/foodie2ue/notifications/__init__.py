from flask_mail import Mail, Message

from flask import render_template, render_template_string

mail = None


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
    mail.send(msg)
