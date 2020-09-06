from flask import Flask, session, url_for, redirect, request
from requests_oauthlib import OAuth1
import requests
import urllib
import sys
import os


args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
request_url = 'https://www.hatena.com/oauth/initiate'
authorize_url = 'https://www.hatena.ne.jp/oauth/authorize'
access_token_url = 'https://www.hatena.com/oauth/token'
photo_url = "http://f.hatena.ne.jp/atom/post"
# path_to_file = args[1]
# image_title = args[2]

app = Flask(__name__)
app.secret_key = "aaa"

@app.route('/')
def main():
    access_token = session.get('access_token')
    if access_token:
        return access_token
    else:
        return "error"

@app.route('/login')
def login():
    auth = OAuth1(consumer_key, consumer_secret, callback_uri=url_for('get_request_token', _external=True))
    app.logger.debug("auth: {}".format(vars(auth)))

    req = requests.post(request_url, auth=auth)
    app.logger.debug("request_token:{}".format(urllib.parse.parse_qsl(req.text)))
    request_token = dict(urllib.parse.parse_qsl(req.text))
    session['request_token'] = request_token
    return redirect("{}?oauth_token={}".format(authorize_url, session['request_token']['oauth_token']))

@app.route('/get_request_token')
def get_request_token():
    request_token = session.get('request_token')
    oauth_verifier = request.args['oauth_verifier']

    auth = OAuth1(consumer_key, consumer_secret, request_token['oauth_token'], request_token['oauth_token_secret'], verifier=oauth_verifier)
    req = requests.post(access_token_url, auth=auth)
    access_token = dict(urllib.parse.parse_qsl(req.text))

    if session.get('request_token'): session.pop('request_token')
    session['access_token']=access_token

    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(port=8000, debug=True)