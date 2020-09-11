import os
import base64
import requests
import datetime
import hashlib
import random
from bs4 import BeautifulSoup
import re


class PostHatena:
    def __init__(self, endpoint, dir_path, file_filter_pattern, xml_template, hatena_id, api_key):
        self.endpoint = endpoint
        self.dir_path = dir_path
        self.file_filter_pattern = file_filter_pattern 
        self.xml_template = xml_template
        self.hatena_id = hatena_id
        self.api_key = api_key

    def extract_file_path(self):
        file_paths = [ self.dir_path + f for f in os.listdir(self.dir_path) if re.match(self.file_filter_pattern, f, re.IGNORECASE)]
        n_file_paths = '\n'.join(file_paths)
        print(f'''\n---Upload the following file---
{n_file_paths}
\n
If everything is OK, enter "yes" or "y".
If you don\'t like it, enter "no" or "n".
''')
        res = input()
        if not res in ['y', 'yes']:
            if res in ['n', 'no']:
                file_paths = []
                return file_paths
            print('Interrupt processing!')
            exit()
        return file_paths

    def make_xml_post_body(self, file_path):
        title = file_path.split('/')[-1]
        with open(file_path) as f:
            post_body = f.read()
            f.close()
        post_body = post_body.replace("<", "&lt;")
        post_body = post_body.replace(">", "&gt;")
        xml_post_body = self.xml_template.format(title, self.hatena_id, post_body,)
        return xml_post_body

    def create_auth_headers(self):
        headers = {}
        basic_user_and_password = base64.b64encode('{}:{}'.format(self.hatena_id, self.api_key).encode()).decode()
        headers['Authorization'] = 'Basic ' + basic_user_and_password
        return headers

    def post_to_hatena(self, xml_post_body, headers):
        bytes_xml_post_body = xml_post_body.encode()
        res = requests.post(url=self.endpoint, data=bytes_xml_post_body, headers=headers)
        if not res.status_code == 201:
            print(f'''-----
Status Code:{res.status_code}
{res.text}
-----
''')
        soup = BeautifulSoup(res.content, 'xml')
        response_url = soup.find('link').get('href')
        print(f'''-----
Success!
URL: {response_url}
-----
''')
        return response_url

class PostHatenaPhoto(PostHatena):
    def make_xml_post_body(self, file_path):
        title = file_path.split('/')[-1]
        upload_foleder = re.search(r'[^\/]*\/assets', self.dir_path).group().split('/')[0]
        with open(file_path, 'br') as f:
            post_body = f.read()
            f.close()
            post_body = base64.b64encode(post_body).decode()
        xml_post_body = self.xml_template.format(title, post_body, upload_foleder)
        return xml_post_body

    def create_auth_headers(self):
            headers = {}
            created = datetime.datetime.now().isoformat() + 'Z'
            nonce = hashlib.sha1(str(random.random()).encode()).digest()
            password_digest = hashlib.sha1(nonce + created.encode() + self.api_key.encode()).digest()
            password_digest_base64 = base64.b64encode(password_digest).decode()
            nonce_base64 = base64.b64encode(nonce).decode()
            wsse = f'UsernameToken Username="{self.hatena_id}", PasswordDigest="{password_digest_base64}", Nonce="{nonce_base64}", Created="{created}"'
            headers['X-WSSE'] = wsse
            return headers







