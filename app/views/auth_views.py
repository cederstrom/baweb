from flask import redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user
from app import app, lm, oauth
from app.models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route("/login")
def login():
    redirect_uri = url_for('login_callback', _external=True)
    params = {'redirect_uri': redirect_uri, 'scope': 'email'}
    return redirect(oauth.get_authorize_url(params))


@app.route("/loginCallback")
def login_callback():
    print("Entering authorized")
    if 'code' in request.args:
        redirect_uri = url_for('login_callback', _external=True)
        data = dict(code=request.args['code'], redirect_uri=redirect_uri)
        session = oauth.get_auth_session(data=data)
        me = session.get('me').json()
        email = me['email']
        user = User.get_from_email(email)
        if user:
            login_user(user)
            print('Logged in as %r' % user)
            return redirect(url_for('index'))
        else:
            print('No user found for email %r' % email)
    else:
        print('User did not authorize the request')
    return redirect(url_for('logout'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
