import os
import sys
import logging
import traceback
import base64
import requests
from requests_oauthlib import OAuth1
import urllib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
oauth_request_url = 'https://www.hatena.com/oauth/initiate'
oauth_authorize_url = 'https://www.hatena.ne.jp/oauth/authorize'
oauth_access_token_url = 'https://www.hatena.com/oauth/token'
request_url = "http://f.hatena.ne.jp/atom/post"
path_to_file = args[1]
image_title = args[2]

def get_access_token()

def get_oauth():
    # auth = OAuth1(consumer_key, consumer_secret)
    # callback_uri="authorize"
    auth = OAuth1(consumer_key, consumer_secret, callback_uri="oob")
    req = requests.post(oauth_request_url, auth=auth)
    print(req.headers)
    print(dict(urllib.parse.parse_qsl(req.text)))
    request_token = dict(urllib.parse.parse_qsl(req.text))
    req = requests.get('%s?oauth_token=%s&perms=delete' % (oauth_authorize_url, request_token['oauth_token']))
    print(dict(urllib.parse.parse_qsl(req.text)))

    # ユーザ許可後に表示される、PINコードを入力する
    # oauth_verifier = input("Please input PIN code:")
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        verifier=request_token['oauth_verifier'])

    r = requests.post(oauth_access_token_url, auth=auth)

    access_token = dict(urllib.parse.parse_qsl(r.text))
    return access_token

def make_xml_post_body():
    with open(path_to_file, 'br') as image_file:
        image_data = base64.b64encode(image_file.read())
        image_file.close
    xml_post_body = f"""<entry xmlns="http://purl.org/atom/ns#">
  <title>{image_title}</title>
  <content mode="base64" type="image/png">{image_data}</content>
</entry>"""
    return xml_post_body

def post_to_hatena_api(xml_post_body):
    bytes_xml_post_body = xml_post_body.encode("UTF-8")
    basic_user_and_password = base64.b64encode("{}:{}".format(hatena_id, api_key).encode("utf-8"))
    headers = {}
    headers["Content-type"] = "application/x-www-form-urlencoded"
    logger.debug('---headers---')
    logger.debug(headers)
    req = requests.post(url=request_url, data=bytes_xml_post_body, headers=headers, auth=(hatena_id, api_key))
    # logger.debug('---HTTP Response---')
    # logger.debug(req.status_code)
    # logger.debug(req.text)
    print('---HTTP Response---')
    print(req.status_code)
    print(req.text)

def main():
    get_oauth()
    xml_post_body = make_xml_post_body()
    post_to_hatena_api(xml_post_body)

if __name__ == '__main__':
    main()