import urllib.request
import os
import sys
import logging
import traceback
import requests
import oauth2 as oauth
import sqlite3
import cgi
import cgitb

cgitbb.enable()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
request_token_url = os.environ['REQUEST_TOKEN_URL']


request_url = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry"
path_to_file = args[1]
blog_title = args[2]

def parseqsl(url):
    param = {}
    for i in url.split('&'):
        _p = i.split('=')
        param.update({_p[0]: _p[1]})
    return param
def get_oauth():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    # Get Request Token
    resp, content = clinet.request(request_token_url, 'GET')
    request_token = dicet(parse_qsl(content))

    # 認証ページに遷移
    url = '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])

    # request_token と request_token_secret を保存
    con = sqlite3.connect('oauth.db')
    con.execute(u'insert into oauth values (?, ?)', (request_token['oauth_token'], request_token['oauth_token_secret']))
    con.commit()
    con.close()

def callback():
    # oauth_token と oauth_verifier を取得
    if 'QUERY_STRING' in os.environ:
        query = cgi.parse_qs(os.environ['QUERY_STRING'])
    else:
        query = {}

    # oauth_token_secret を取得
    con = sqlite3.connect('oauth.db')
    oauth_token_secret = con.execute(
        u'select oauth_token_secret from oauth where oauth_token = ?'
        , [query['oauth_token'][0]]).fetchone()[0]
    con.close()

    # Access_token と access_token_secret を取得
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(query['oauth_token'][0], query['oauth_verifier'][0])
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST", body="oauth_verifier=%s" % query['oauth_verifier'][0])
    access_token = dict(parse_qsl(content))

    return access_token['oauth_token'], access_token['oauth_token_secret']

def make_xml_post_body():
    with open(path_to_file) as f:
        xml_post_body = f.read()
        f.close()
    xml_post_body = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{blog_title}</title>
  <author><name>{hatena_id}</name></author>
  <content type="text/x-markdown">
    {xml_post_body}
  </content>
  <category term="AWS" />
  <app:control>
    <app:draft>yes</app:draft>
  </app:control>
</entry>"""
    logger.debug('---xml_post_body---')
    logger.debug(xml_post_body)
    return xml_post_body
        
def post_to_hatena_api(xml_post_body, access_token, access_token_secret):
    bytes_xml_post_body = xml_post_body.encode("UTF-8")
    basic_user_and_password = base64.b64encode("{}:{}".format(hatena_id, api_key).encode("utf-8"))
    headers = {}
    headers["Content-type"] = "application/x-www-form-urlencoded"
    logger.debug('---headers---')
    logger.debug(headers)
    req = requests.post(url=request_url, data=bytes_xml_post_body, headers=headers, auth=(hatena_id, api_key))
    logger.debug('---HTTP Response---')
    logger.debug(req.status_code)
    logger.debug(req.text)

def main():
    try:
        logger.debug('---request_url----')
        logger.debug(request_url)
        get_oauth()
        access_token, access_token_secret = callback()       
        xml_post_body = make_xml_post_body()
        post_to_hatena_api(xml_post_body, access_token, access_token_secret)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

if __name__=='__main__':
    main()
