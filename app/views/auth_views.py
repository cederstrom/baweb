from flask import redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user
from app import app, lm
from app.models import User
from authlib.integrations.flask_client import OAuth
import json

oauth = OAuth(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route("/login")
def login():
                    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = app.config['FB_CLIENT_ID']
    FACEBOOK_CLIENT_SECRET = app.config['FB_CLIENT_SECRET']
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('login_callback', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route("/loginCallback")
def login_callback():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name')
    profile = resp.json()
    print("Facebook User ", profile)

    facebook_id = profile['id']
    user = User.get_from_facebook_id(int(facebook_id))
    if user != None:
        login_user(user)
        print('Logged in as %r' % user)
        return redirect(url_for('index'))
    else:
        print('No user found or user did not authorize the request')
        return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
