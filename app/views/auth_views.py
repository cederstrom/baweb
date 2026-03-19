from flask import redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from app import app, lm, oauth
from app.models import User
import json
from uuid import uuid4

from google_auth_oauthlib.flow import Flow

@app.route('/googleverify/google0ca3c9a75862042e.html')
def google_site_verification():
    return (
        'google-site-verification: google0ca3c9a75862042e.html',
        200,
        {'Content-Type': 'text/html; charset=utf-8'}
    )

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def _build_google_flow(code_verifier=None):
    return Flow.from_client_secrets_file(
        app.config['GOOGLE_OAUTH_CLIENT_SECRETS_FILE'],
        scopes=GMAIL_SCOPES,
        redirect_uri=app.config['GOOGLE_OAUTH_REDIRECT_URI'],
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
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())

    session_id = session['session_id']

@app.route("/login")
def login():
    redirect_uri = url_for('login_callback', _external=True)
    params = {'redirect_uri': url_for('login_callback', _external=True)}
    return redirect(oauth.get_authorize_url(params))

@app.route("/loginCallback")
def login_callback():
    if 'code' in request.args:
        redirect_uri = url_for('login_callback', _external=True)
        data = dict(code=request.args['code'], redirect_uri=redirect_uri)
        oauth_session = oauth.get_auth_session(data=data, decoder=json.loads)
        me = oauth_session.get('me').json()
        try:
            print(json.dumps(me, sort_keys=True, indent=4, separators=(',', ': ')))
        except Exception as error:
            print(error)
        try:
            email = me['email']
            user = User.get_from_email(email)
        except Exception as error_email:
            print('No user found by email: %r' % error_email)
            print('Trying with facebook_id...')
            try:
                facebook_id = me['id']
                user = User.get_from_facebook_id(int(facebook_id))
            except Exception as error_facebook_id:
                print('No user found by facebook_id: %r' % error_facebook_id)

        if user:
            user.session_id = session['session_id']
            login_user(user)
            print('Logged in as %r' % user)
            return redirect(url_for('index'))
        else:
            print('No user found')
    else:
        print('User did not authorize the request')
    return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        current_user.session_id = None
    logout_user()
    session.clear()
    return redirect(url_for('index'))
