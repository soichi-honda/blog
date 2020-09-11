import traceback
from post_hatena import PostHatena, PostHatenaPhoto
import os
import sys
import re

args = sys.argv

hatena_id = os.environ['HATENA_ID']
blog_id = os.environ['BLOG_ID']
api_key = os.environ['API_KEY']

dir_path = args[1]
if not re.match(r'.*?\/$', dir_path):
    dir_path = dir_path + '/'

def upload_text():
    text_endpoint = f'https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry'
    text_file_filter_pattern = r'.*?\.md'
    text_xml_template = '''<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{}</title>
  <author><name>{}</name></author>
  <content type="text/x-markdown">{}</content>
  <category term="" />
  <app:control>
    <app:draft>yes</app:draft>
  </app:control>
</entry>'''

    post_hatena = PostHatena(endpoint=text_endpoint, dir_path=dir_path, file_filter_pattern=text_file_filter_pattern, xml_template=text_xml_template, hatena_id=hatena_id, api_key=api_key)
    text_file_paths = post_hatena.extract_file_path()
    if text_file_paths:
        xml_post_body = post_hatena.make_xml_post_body(text_file_paths[0])
        headers = post_hatena.create_auth_headers()
        response_url = post_hatena.post_to_hatena(xml_post_body, headers)
    return

def upload_images():
    photo_endpoint = 'https://f.hatena.ne.jp/atom/post/'
    image_dir_path = dir_path + 'assets/'
    image_file_filter_pattern = r'.*?\.png'
    photo_xml_template = '''<entry xmlns="http://purl.org/atom/ns#">
  <title>{}</title>
  <content mode="base64" type="image/png">{}</content>
  <dc:subject>{}</dc:subject>
</entry>'''
    post_hatena_photo = PostHatenaPhoto(endpoint=photo_endpoint, dir_path=image_dir_path, file_filter_pattern=image_file_filter_pattern, xml_template=photo_xml_template, hatena_id=hatena_id, api_key=api_key)
    image_file_paths = post_hatena_photo.extract_file_path()
    if image_file_paths:
        headers = post_hatena_photo.create_auth_headers()
        for image_file_path in image_file_paths:
            xml_post_body = post_hatena_photo.make_xml_post_body(image_file_path)
            response_url = post_hatena_photo.post_to_hatena(xml_post_body, headers)
    return

def main():
    try:
        upload_text()
        print('''Want to uploading images?
\n
If you want, enter "yes" or "y".
If you don\'t want it, enter "no" or "n".
''')
        res = input()
        if not res in ['y', 'yes']:
            if res in ['n', 'no']:
                return
            print('Interrupt processing!')
            exit()
        upload_images()
        print('All Done.')
    except Exception as e:
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
    print('\nGood bye!')
