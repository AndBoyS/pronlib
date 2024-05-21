import random
from typing import Iterator

import pytest

from src.app.const import DEBUG_CACHE_PATH, OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.app.opener import Cache, leave_uncached_media, get_all_media, get_random_media
from src.const import PHOTO_PATH, VIDEO_PATH


@pytest.fixture
def cmds_cache() -> Iterator[Cache]:
    DEBUG_CACHE_PATH.unlink(missing_ok=True)
    cmds_cache = Cache(DEBUG_CACHE_PATH)
    yield cmds_cache
    DEBUG_CACHE_PATH.unlink()


def test_cmd_gen(cmds_cache: Cache) -> None:
    random.seed(69)
    open_photo_cmd_no_path = OPEN_PHOTO_CMD.replace('"{path}', "")
    open_video_cmd_no_path = OPEN_VIDEO_CMD.replace('"{path}', "")

    medias = get_all_media(video_path=VIDEO_PATH, photo_path=PHOTO_PATH)
    num_media = len(medias)

    for _ in range(2):
        for i in range(num_media):
            assert len(leave_uncached_media(medias=medias, media_cache=cmds_cache)) == num_media - i
            media = get_random_media(medias=medias, media_cache=cmds_cache)
            assert open_photo_cmd_no_path in media.open_cmd or open_video_cmd_no_path in media.open_cmd
