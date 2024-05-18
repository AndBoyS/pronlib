import random
from natsort import natsorted

from src.app.const import OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.const import PHOTO_PATH, VIDEO_PATH
from src.media_indexing.folder_index import MediaChapter, PhotoChapter, Video, VideoChapter, get_subfolders


def generate_open_cmds() -> list[str]:
    video_folders = natsorted(get_subfolders(VIDEO_PATH))
    photo_folders = natsorted(get_subfolders(PHOTO_PATH))

    video_chapters: list[MediaChapter] = [VideoChapter(path) for path in video_folders]
    photo_chapters: list[MediaChapter] = [PhotoChapter(path) for path in photo_folders]

    chapters = video_chapters + photo_chapters
    medias = [media for chapter in chapters for media in chapter.media_list]

    cmds: list[str] = []
    for media in medias:
        if isinstance(media, Video):
            cmd = OPEN_VIDEO_CMD.replace("{path}", str(media.path))
        else:
            first_photo = natsorted(media.path.iterdir())[0]
            cmd = OPEN_PHOTO_CMD.replace("{path}", str(first_photo))
        cmds.append(cmd)

    return cmds


def get_random_open_cmd() -> str:
    return random.choice(generate_open_cmds())
