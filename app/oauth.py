from app import app
from rauth.service import OAuth2Service


graph_url = app.config['FACEBOOK_GRAPH_URL']
facebook = OAuth2Service(name='facebook',
                         authorize_url='https://www.facebook.com/dialog/oauth',
                         access_token_url=graph_url + 'oauth/access_token',
                         client_id=app.config['FB_CLIENT_ID'],
                         client_secret=app.config['FB_CLIENT_SECRET'],
                         base_url=graph_url)


def get_authorize_url(params):
    return facebook.get_authorize_url(**params)


def get_auth_session(data):
    return facebook.get_auth_session(data=data)
