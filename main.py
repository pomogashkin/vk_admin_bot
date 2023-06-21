import vk_api
from vk_api.audio import VkAudio
from tqdm import tqdm
from pinscrape import pinscrape

import random
import os
import requests
import time 
import datetime

from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('URL')
ME = os.getenv('ME')

def delete_trash(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    

def get_word():
    try:
        response = requests.get(URL)
    except Exception:
        time.sleep(10)
        response = requests.get(URL)

    response = response.json()
    word = response[0]
    return word

def get_img():
    delete_trash('./output/')
    details = None
    word = get_word()
    details = pinscrape.scraper.scrape(word, "output", {}, 10, 5)
    if len(os.listdir('./output/')) != 5:
        get_img()

        
    if details["isDownloaded"]:
        print("\nDownloading completed !!")
        print(f"\nTotal urls found: {len(details['extracted_urls'])}")
        print(f"\nTotal images downloaded (including duplicate images): {len(details['url_list'])}")
        print(details)
    else:
        print("\nNothing to download !!")
    return word

def get_tracks(vk_session, owner):
    return [item['id'] for item in tqdm(VkAudio(vk_session).get_iter(owner_id=owner))]


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

def main():
    login, password = os.getenv('LOGIN'), os.getenv('PASSWORD')
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    
    tracks = get_tracks(vk_session, ME)
    last_update = datetime.datetime.now()
    upload = vk_api.VkUpload(vk_session)
    
    while True:
        attachments = f'audio{ME}_{random.choice(tracks)}'
        word = get_img()
        for item in os.listdir('./output/'):
            photo = upload.photo( 
                f'./output/{item}',
                album_id=295514739,
                group_id=221221426
            )
            attachments += ',photo-221221426_{}'.format(str(photo[0]['id']))
        
        
        print(
            vk_session.get_api().wall.post(
                owner_id=-221221426, 
                message=word, 
                attachments=attachments
            )
        )
        if datetime.datetime.now() == last_update + datetime.timedelta(7):
            tracks = get_tracks(vk_session)
            last_update = datetime.datetime.now()
        time.sleep(3600)


if __name__ == '__main__':
    main()