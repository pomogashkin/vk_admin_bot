import datetime
import os
import random
import time

import requests
import vk_api
from dotenv import load_dotenv
from pinscrape import pinscrape
from tqdm import tqdm
from vk_api.audio import VkAudio

load_dotenv()

GROUP = os.getenv('GROUP')
URL = os.getenv('URL')
ME = os.getenv('ME')
ALBUM_ID = os.getenv('ALBUM_ID')

def delete_trash(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    

def get_word():
    """Получение случайного слова

    Returns:
        str: случайное слово
    """    
    try:
        response = requests.get(URL)
    except Exception:
        time.sleep(10)
        get_word()

    response = response.json()
    return response[0]

def get_img():
    """Скачивание 5 случайных картинок по случайному слову

    Returns:
        str: случайное слово
    """    
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
    """Получение списка  id всех добавленных песен пользователя

    Args:
        vk_session (_type_): сессия 
        owner (_type_): пользователь

    Returns:
        list: список id песен
    """    
    tracks = []
    try: 
        for item in tqdm(VkAudio(vk_session).get_iter(owner_id=owner)):
            tracks.append(item['id'])
    except Exception as error:
        print(error)
        pass
        
    return tracks


def auth_handler(): 
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

def main():
    """
    Главная функция.
    """
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
                album_id=ALBUM_ID,
                group_id=GROUP
            )
            attachments += ',photo{}_{}'.format(GROUP, str(photo[0]['id']))
        
        
        print(
            vk_session.get_api().wall.post(
                owner_id=GROUP, 
                message=word, 
                attachments=attachments
            )
        )
        if datetime.datetime.now() == last_update + datetime.timedelta(7):
            tracks = get_tracks(vk_session)
            last_update = datetime.datetime.now()
        time.sleep(3600 * 3)


if __name__ == '__main__':
    main()