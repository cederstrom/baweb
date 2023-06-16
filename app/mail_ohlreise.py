# -*- coding: utf-8 -*-
from app import app
import smtplib
from email.mime.text import MIMEText


FROM_ADDRESS = 'info.brutalakademien'
SUBJECT = "Bokningskonfirmation"
BODY = """
Tack för din anmälan!

Priset du får pröjsa för Öhlreise är %r kr.
Vänligen sätt in pangarna på vårt pengartvättarkonto hos %r på kontonummer %r senast %r. Märk betalningen med ditt namn (%r).

Om du upptäcker att något blev fel så är det bara att svara på det här mailet.

--
Brutal Akademien
Ne Sedibus Rotalibus Ludas
"""


def send(to_address="andreas.cederstrom@gmail.com", price=1337,
         team_name="Aporna"):
    bank = app.config['ÖHLREISE']['payment']['bank']
    account_number = app.config['ÖHLREISE']['payment']['account_number']
    last_payment_date = app.config['ÖHLREISE']['payment']['last_payment_date']
    mail = _build_mail(to_address, price, bank, account_number, last_payment_date, team_name)
    _do_send(mail)


def _build_mail(to_address, price, bank, account_number, last_payment_date , team_name):
    body = BODY % (price, bank, account_number, last_payment_date, team_name)
    mail = MIMEText(body)
    mail['Subject'] = SUBJECT
    mail['From'] = FROM_ADDRESS
    mail['To'] = to_address
    return mail


def _do_send(mail):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(app.config['GMAIL_USERNAME'], app.config['GMAIL_PASSWORD'])
    server.sendmail(mail['From'], mail['To'], mail.as_string())
    server.quit()
