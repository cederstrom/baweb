from flask import redirect, url_for, request, session
from flask_login import login_user, logout_user
from app.models import User
from app import app, lm, db

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

@app.route('/google0ca3c9a75862042e.html')
def google_site_verification():
    return (
        'google-site-verification: google0ca3c9a75862042e.html',
        200,
        {'Content-Type': 'text/html; charset=utf-8'}
    )

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
LOGIN_SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']


def _build_google_flow(code_verifier=None):
    return Flow.from_client_secrets_file(
        app.config['GOOGLE_OAUTH_CLIENT_SECRETS_FILE'],
        scopes=GMAIL_SCOPES,
        redirect_uri=app.config['GOOGLE_OAUTH_REDIRECT_URI'],
        code_verifier=code_verifier
    )


def _build_login_flow(code_verifier=None):
    return Flow.from_client_secrets_file(
        app.config['GOOGLE_LOGIN_CLIENT_SECRETS_FILE'],
        scopes=LOGIN_SCOPES,
        redirect_uri=app.config['GOOGLE_LOGIN_REDIRECT_URI'],
        code_verifier=code_verifier
    )


@app.route('/admin/gmail/connect')
def gmail_connect():
    setup_key = request.args.get('key')
    if setup_key != app.config['GMAIL_OAUTH_SETUP_KEY']:
        return "Forbidden", 403

    flow = _build_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
        code_challenge_method='S256'
    )

    session['gmail_oauth_state'] = state
    session['gmail_oauth_code_verifier'] = flow.code_verifier

    return redirect(authorization_url)


@app.route('/admin/gmail/oauth/callback')
def gmail_oauth_callback():
    state = session.get('gmail_oauth_state')
    code_verifier = session.get('gmail_oauth_code_verifier')

    if not state:
        return "Missing OAuth state", 400

    if not code_verifier:
        return "Missing OAuth code verifier", 400

    flow = _build_google_flow(code_verifier=code_verifier)

    flow.fetch_token(
        authorization_response=request.url
    )

    creds = flow.credentials
    token_path = app.config['GOOGLE_OAUTH_TOKEN_FILE']

    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())

    session.pop('gmail_oauth_state', None)
    session.pop('gmail_oauth_code_verifier', None)

    return "Gmail connected successfully. token.json saved."


@lm.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None


@app.route("/login")
def login():
    flow = _build_login_flow()
    
    authorization_url, state = flow.authorization_url(
        prompt='select_account',
        code_challenge_method='S256'
    )
    session['google_login_state'] = state
    session['google_login_code_verifier'] = flow.code_verifier
    
    return redirect(authorization_url)


@app.route("/login/callback")
def login_callback():
    state = session.get('google_login_state')
    code_verifier = session.get('google_login_code_verifier')

    if not state:
        return "Missing OAuth state", 400

    if not code_verifier:
        return "Missing OAuth code verifier", 400

    flow = _build_login_flow(code_verifier=code_verifier)
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        google_requests.Request(),
        audience=app.config['GOOGLE_LOGIN_CLIENT_ID']
    )

    email = id_info.get('email')
    google_sub = id_info.get('sub')
    
    if not email:
        return redirect(url_for('logout'))

    user = User.get_from_email(email)
    if not user or not user.is_admin:
        return redirect(url_for('logout'))
    

    if google_sub and user.google_id != google_sub:
        user.google_id = google_sub
        db.session.commit()

    login_user(user)

    session.pop('google_login_state', None)
    session.pop('google_login_code_verifier', None)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))