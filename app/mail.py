from app import app
import smtplib
from email.mime.text import MIMEText


FROM_ADDRESS = 'admin@brutal-akademien.org'
SUBJECT = "Bokningskonfirmation"
BODY = """
Tack för din anmälan!

Priset ni betalar för Flumride är %r kr.
Vänligen sätt in pangarna på vårt pengartvättarkonto hos Nordea på kontonummer 1111,3103450 senast 2015-04-20. Märk betalningen med ert lagnamn (%r).

Om du upptäcker att något blev fel så är det bara att svara på det här mailet.

--
Brutal Akademien
Ne Sedibus Rotalibus Ludas
"""


def send(to_address="andreas.cederstrom@gmail.com", price=1337,
         team_name="Aporna"):
    mail = _build_mail(to_address, price, team_name)
    _do_send(mail)


def _build_mail(to_address, price, team_name):
    body = BODY % (price, team_name)
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
