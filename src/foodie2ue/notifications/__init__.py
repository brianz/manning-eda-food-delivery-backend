from flask_mail import Mail, Message

from flask import render_template, render_template_string

mail = None


def setup_mail(app):
    global mail
    mail = Mail(app)


plain_text = """
Thanks for your order {{ first_name }}!

Your order number is {{ order_number }} and the total is ${{ order_total }}.

The kitchen will start preparing your order soon and drivers have been notified.

Sincerely,
The Foodie2ue team
"""


def send_message(recipient, first_name, order_id, order_total) -> None:
    template_args = {
        'first_name': first_name,
        'order_id': order_id,
        'order_total': order_total,
    }
    html_body = render_template('email-template.html.j2', **template_args)
    text_body = render_template_string(plain_text, **template_args)

    if recipient not in ('brianz@gmail.com', 'matt.d.diamond@hotmail.com'):
        recipient = 'brianz@gmail.com'

    msg = Message(
        subject="Thanks for your order!",
        recipients=[recipient],
        html=html_body,
        body=text_body,
    )
    mail.send(msg)
