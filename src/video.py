import json

from src.settings import BaseAPI


class Video(BaseAPI):
    """Класс для представления ютуб видео."""

    def __init__(self, id_: str) -> None:
        self._id: str = id_

        self._json_: dict = self.get_youtube_json()
        self._json_item_: dict = self._json_['items'][0]

        self._title: str = self._json_item_['snippet']['title']
        self._url: str = f'https://www.youtube.com/watch?v={self._id}'
        self._views_count: int = int(self._json_item_['statistics']['viewCount'])
        self._likes_count: int = int(self._json_item_['statistics']['likeCount'])

    def get_youtube_json(self):
        response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                              id=self._id).execute()
        return response

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.get_youtube_json(), indent=4, ensure_ascii=False))

    def __repr__(self) -> str:
        lst = ', '.join(['{0}={1}'.format(k, v if str(v).isdigit() else f"'{v}'")
                         for k, v in self.__dict__.items()
                         if not k.endswith('_')])

        return f'{self.__class__.__name__}({lst})'

    def __str__(self) -> str:
        return f'{self._title}'


class PLVideo:
    pass


if __name__ == '__main__':
    # Создаем два экземпляра класса
    video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
    # video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    assert str(video1) == 'GIL в Python: зачем он нужен и как с этим жить'
    # assert str(video2) == 'MoscowPython Meetup 78 - вступление'
    # print(repr(video1))


