import urllib.request
import os
import sys
import logging
import traceback
import base64
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
api_key = os.environ['API_KEY']
request_url = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry"
path_to_file = args[1]
blog_title = args[2]

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
        
def post_to_hatena_api(xml_post_body):
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
        xml_post_body = make_xml_post_body()
        post_to_hatena_api(xml_post_body)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

if __name__=='__main__':
    main()
