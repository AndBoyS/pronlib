import atexit
import functools
from pathlib import Path
import pickle
import random
from natsort import natsorted

from src.app.const import OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.media_indexing.folder_index import Media, Video, get_chapters


class Cache:
    def __init__(self, path: Path) -> None:
        self.cache = self.get_cache(path)

    @staticmethod
    @functools.cache  # Для идентичности объектов кэша при повторном вызове
    def get_cache(path: Path) -> set[str]:
        """
        Получить set, который будет кэшироваться в path
        В течение работы программы данные хранятся в ОЗУ: выгрузка осуществляется при завершении программы
        """

        def load() -> set[str]:
            with path.open("rb") as file:
                try:
                    res: set[str] = pickle.load(file)
                    return res
                except EOFError:
                    return set()

        def dump(cache: set[str]) -> None:
            with path.open("wb") as file:
                pickle.dump(cache, file)

        path.touch(exist_ok=True)
        cache = load()
        atexit.register(lambda: dump(cache))

        return cache

    def add_new_el(self, cmd: str) -> None:
        self.cache.add(cmd)

    def reset_cache(self) -> None:
        self.cache.clear()


def get_all_media(video_path: Path, photo_path: Path) -> list[Media]:
    video_chapters, photo_chapters = get_chapters(video_path=video_path, photo_path=photo_path)

    chapters = video_chapters + photo_chapters
    medias = [media for chapter in chapters for media in chapter.media_list]
    return medias


def generate_open_cmds(medias: list[Media], cmds_cache: Cache) -> list[str]:
    cmds: list[str] = []
    for media in medias:
        if isinstance(media, Video):
            cmd = OPEN_VIDEO_CMD.replace("{path}", str(media.path))
        else:
            cmd = OPEN_PHOTO_CMD.replace("{path}", str(media.first_file_path))
        cmds.append(cmd)

    cached_cmds = cmds_cache.cache
    new_cmds = natsorted(set(cmds) - cached_cmds)

    if not new_cmds:
        cmds_cache.reset_cache()
        return cmds

    return new_cmds


def get_random_open_cmd(medias: list[Media], cmds_cache: Cache) -> str:
    cmd = random.choice(generate_open_cmds(medias=medias, cmds_cache=cmds_cache))
    cmds_cache.add_new_el(cmd)
    return cmd
