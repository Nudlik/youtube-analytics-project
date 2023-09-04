import os

from googleapiclient.discovery import build


class BaseAPI:
    """ Базовый класс для работы с API """
    YT_API_KEY = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
