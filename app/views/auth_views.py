from flask import redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from app import app, lm, oauth
from app.models import User
import json
from uuid import uuid4

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
