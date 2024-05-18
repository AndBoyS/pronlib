import random
from src.app.const import OPEN_PHOTO_CMD, OPEN_VIDEO_CMD
from src.app.opener import generate_open_cmds, get_random_open_cmd


def test_cmd_gen() -> None:
    random.seed(69)
    cmd = get_random_open_cmd()
    assert isinstance(cmd, str)

    for cmd in generate_open_cmds():
        assert OPEN_PHOTO_CMD.replace('"{path}"', "") in cmd or OPEN_VIDEO_CMD.replace('"{path}"', "") in cmd
