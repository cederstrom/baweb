# -*- coding: utf-8 -*-
import os
import json
import base64
from email.mime.text import MIMEText

from app import app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

SUBJECT = "Bokningskonfirmation"
BODY = """
Tack för din anmälan!

Priset ni betalar för Flumride är %r kr.
Vänligen sätt in pangarna på vårt pengartvättarkonto hos %r via Swish till %r senast %r. Märk betalningen med ert lagnamn (%r).

Om du upptäcker att något blev fel så är det bara att svara på det här mailet.

--
Brutal-Akademien
Ne Sedibus Rotalibus Ludas
"""


def send(to_address="andreas.cederstrom@gmail.com", price=1337, team_name="Aporna"):
    bank = app.config['FLUMRIDE']['payment']['bank']
    account_number = app.config['FLUMRIDE']['payment']['account_number']
    last_payment_date = app.config['FLUMRIDE']['payment']['last_payment_date']

    subject, body = _build_mail_content(
        price,
        bank,
        account_number,
        last_payment_date,
        team_name
    )
    _do_send(to_address, subject, body)


def _build_mail_content(price, bank, account_number, last_payment_date, team_name):
    body = BODY % (price, bank, account_number, last_payment_date, team_name)
    return SUBJECT, body


def _load_credentials():
    token_path = app.config['GOOGLE_OAUTH_TOKEN_FILE']

    if not os.path.exists(token_path):
        raise RuntimeError("Gmail OAuth token.json is missing. Connect Gmail via the admin OAuth route first.")

    with open(token_path, 'r') as f:
        token_data = json.load(f)

    creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_credentials(creds)

    if not creds.valid:
        raise RuntimeError("Gmail OAuth credentials are invalid. Reconnect Gmail.")

    return creds


def _save_credentials(creds):
    token_path = app.config['GOOGLE_OAUTH_TOKEN_FILE']
    with open(token_path, 'w') as f:
        f.write(creds.to_json())


def _build_gmail_service():
    creds = _load_credentials()
    return build('gmail', 'v1', credentials=creds)


def _create_message(to_address, subject, body):
    from_address = app.config['GMAIL_FROM_ADDRESS']

    message = MIMEText(body, _charset='utf-8')
    message['To'] = to_address
    message['From'] = from_address
    message['Subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}


def _do_send(to_address, subject, body):
    service = _build_gmail_service()
    message = _create_message(to_address, subject, body)

    service.users().messages().send(
        userId='me',
        body=message
    ).execute()