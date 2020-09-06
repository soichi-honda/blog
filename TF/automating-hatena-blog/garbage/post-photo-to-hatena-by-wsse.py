import os
import sys
# import logging
import traceback
import base64
import requests
import datetime
import hashlib
import random
from bs4 import BeautifulSoup
import re

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
api_key = os.environ['API_KEY']

endpoint = "https://f.hatena.ne.jp/atom/post/"

upload_folder = args[1]
image_dir_path = args[2]
if not re.match(r'.*?\/$', image_dir_path):
    image_dir_path = image_dir_path + '/'

def extract_image_files():
    files = os.listdir(image_dir_path)
    image_files = [ image_dir_path + image_file for image_file in files if os.path.isfile(image_dir_path + image_file)]
    print(f"""---Image_files---
\n
{image_files}
----------
If everything is OK, enter "ok".
If you don\'t like it, enter "no".
""")
    res = input()
    if res == "ok":
        return image_files
    elif res == "no":
        print('Interrupt processing!')
        exit()
    else:
        print('Interrupt processing!')
        exit()

def create_wsse():
    created = datetime.datetime.now().isoformat() + "Z"
    nonce = hashlib.sha1(str(random.random()).encode()).digest()
    password_digest = hashlib.sha1(nonce + created.encode() + api_key.encode()).digest()
    password_digest_base64 = base64.b64encode(password_digest).decode()
    nonce_base64 = base64.b64encode(nonce).decode()
    wsse = f'UsernameToken Username="{hatena_id}", PasswordDigest="{password_digest_base64}", Nonce="{nonce_base64}", Created="{created}"'

    return wsse

def make_xml_post_body(image_file):
    image_title = image_file.split('/')[-1]
    print(f'Image:{image_title}')
    with open(image_file, 'br') as image_file:
        image_data = base64.b64encode(image_file.read()).decode()
        image_file.close
    xml_post_body = f"""<entry xmlns="http://purl.org/atom/ns#">
  <title>{image_title}</title>
  <content mode="base64" type="image/png">{image_data}</content>
  <dc:subject>{upload_folder}</dc:subject>
</entry>"""
    return xml_post_body

def post_to_hatena(xml_post_body, wsse):
    bytes_xml_post_body = xml_post_body.encode()
    headers = {}
    headers["X-WSSE"] = wsse
    res = requests.post(url=endpoint, data=bytes_xml_post_body, headers=headers)
    soup = BeautifulSoup(res.content, 'xml')
    photo_url = soup.find('link').get('href')
    print(f'''-----
Status Code:{res.status_code}
Photo_URL: {photo_url}
-----
''')
    return photo_url.split('/')[-1]

def add_photo_table(image_file, photo_id, photo_table):
    image_title = image_file.split('/')[-1]
    photo_table[image_title] = photo_id
    return photo_table

def main():
    try:
        photo_table = {}
        image_files = extract_image_files()
        wsse = create_wsse()
        i = 1
        for image_file in image_files:
            print(f'{i}. upload start...')
            xml_post_body = make_xml_post_body(image_file)
            photo_id = post_to_hatena(xml_post_body, wsse)
            print(f'{i}. upload end.')
            photo_table = add_photo_table(image_file, photo_id, photo_table)
            i =+1
        print('All uploaded!!')
        print(f'''---Photo Table---
{photo_table}
''')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()