import atexit
import functools
from pathlib import Path
import pickle
import random
from natsort import natsorted

from src.media_indexing.folder_index import Media, get_chapters


class Cache:
    def __init__(self, path: Path) -> None:
        self.cache = self.get_cache(path)

    @staticmethod
    @functools.cache  # Для идентичности объектов кэша при повторном вызове
    def get_cache(path: Path) -> set[Media]:
        """
        Получить set, который будет кэшироваться в path
        В течение работы программы данные хранятся в ОЗУ: выгрузка осуществляется при завершении программы
        """

        def load() -> set[Media]:
            with path.open("rb") as file:
                try:
                    res: set[Media] = pickle.load(file)
                    return res
                except EOFError:
                    return set()

        def dump(cache: set[Media]) -> None:
            with path.open("wb") as file:
                pickle.dump(cache, file)

        path.touch(exist_ok=True)
        cache = load()
        atexit.register(lambda: dump(cache))

        return cache

    def add_new_el(self, media: Media) -> None:
        self.cache.add(media)

    def reset_cache(self) -> None:
        self.cache.clear()

    def __len__(self) -> int:
        return len(self.cache)


def get_all_media(video_path: Path, photo_path: Path) -> list[Media]:
    video_chapters, photo_chapters = get_chapters(video_path=video_path, photo_path=photo_path)

    chapters = video_chapters + photo_chapters
    medias = [media for chapter in chapters for media in chapter.media_list]
    return medias


def leave_uncached_media(medias: list[Media], media_cache: Cache) -> list[Media]:
    uncached_medias = list(set(medias) - media_cache.cache)

    if not uncached_medias:
        media_cache.reset_cache()
        return medias

    return uncached_medias


def get_random_media(medias: list[Media], media_cache: Cache) -> Media:
    medias = leave_uncached_media(medias=medias, media_cache=media_cache)
    media = random.choice(medias)
    media_cache.add_new_el(media)

    return media
