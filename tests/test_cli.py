import random
from typing import Iterator

import pytest

from src.app.const import DEBUG_CACHE_PATH, OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.app.opener import Cache, generate_open_cmds, get_all_media, get_random_open_cmd
from src.const import PHOTO_PATH, VIDEO_PATH


@pytest.fixture
def cmds_cache() -> Iterator[Cache]:
    DEBUG_CACHE_PATH.unlink(missing_ok=True)
    cmds_cache = Cache(DEBUG_CACHE_PATH)
    yield cmds_cache
    DEBUG_CACHE_PATH.unlink()


def test_cmd_gen(cmds_cache: Cache) -> None:
    random.seed(69)

    medias = get_all_media(video_path=VIDEO_PATH, photo_path=PHOTO_PATH)
    all_cmds = generate_open_cmds(medias=medias, cmds_cache=cmds_cache)
    num_cmds = len(all_cmds)

    for _ in range(2):
        for i in range(num_cmds):
            assert len(generate_open_cmds(medias=medias, cmds_cache=cmds_cache)) == num_cmds - i
            cmd = get_random_open_cmd(medias=medias, cmds_cache=cmds_cache)
            assert isinstance(cmd, str)
            assert OPEN_PHOTO_CMD.replace('"{path}"', "") in cmd or OPEN_VIDEO_CMD.replace('"{path}"', "") in cmd
