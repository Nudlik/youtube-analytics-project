import json
from functools import total_ordering

from src.settings import BaseAPI


@total_ordering
class Channel(BaseAPI):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.

        title - название канала
        description - описание канала
        url - ссылка на канал
        subscribers_count - количество подписчиков
        video_count - количество видео
        total_views - общее количество просмотров

        :param channel_id: id канала
        """
        self.__channel_id: str = channel_id

        self.json_: dict = self.get_youtube_json()
        self.json_item: dict = self.json_['items'][0]

        self.title: str = self.json_item['snippet']['title']
        self.description: str = self.json_item['snippet']['description']
        self.url: str = f'https://www.youtube.com/{self.json_item["snippet"]["customUrl"]}'
        self.subscribers_count: int = int(self.json_item['statistics']['subscriberCount'])
        self.video_count: int = int(self.json_item['statistics']['videoCount'])
        self.total_views: int = int(self.json_item['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        dict_to_print = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(dict_to_print, indent=4, ensure_ascii=False))

    def get_youtube_json(self):
        """Возвращает словарь с данными о канале."""
        res = json.dumps(self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
                         indent=4, ensure_ascii=False)
        return json.loads(res)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API вне класса."""
        return cls.youtube

    def to_json(self, file_name: str) -> None:
        """
        Сохраняет данные о канале в файл.

        :param file_name: имя файла
        :return: None
        """
        data = {
            'id_канала': self.__channel_id,
            'название_канала': self.title,
            'описание_канала': self.description,
            'ссылка_на_канал': self.url,
            'количество_подписчиков': self.subscribers_count,
            'количество_видео': self.video_count,
            'общее_количество_просмотров': self.total_views
        }
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def __repr__(self):
        return f'{__class__.__name__}({self.__channel_id})'

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __validate_instance(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

    def __add__(self, other: 'Channel') -> int:
        self.__validate_instance(other)
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other: 'Channel') -> int:
        self.__validate_instance(other)
        return self.subscribers_count - other.subscribers_count

    def __eq__(self, other: 'Channel') -> bool:
        self.__validate_instance(other)
        return self.subscribers_count == other.subscribers_count

    def __lt__(self, other: 'Channel') -> bool:
        self.__validate_instance(other)
        return self.subscribers_count < other.subscribers_count
