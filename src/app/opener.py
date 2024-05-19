import random
from natsort import natsorted

from src.app.const import OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.const import PHOTO_PATH, VIDEO_PATH
from src.media_indexing.folder_index import PhotoChapter, Video, get_chapters


def generate_open_cmds() -> list[str]:
    video_chapters, photo_chapters = get_chapters(VIDEO_PATH, PHOTO_PATH)

    chapters = video_chapters + photo_chapters
    medias = [media for chapter in chapters for media in chapter.media_list]

    cmds: list[str] = []
    for media in medias:
        if isinstance(media, Video):
            cmd = OPEN_VIDEO_CMD.replace("{path}", str(media.path))
        else:
            cmd = OPEN_PHOTO_CMD.replace("{path}", str(media.first_file_path))
        cmds.append(cmd)

    return cmds


def get_random_open_cmd() -> str:
    return random.choice(generate_open_cmds())
