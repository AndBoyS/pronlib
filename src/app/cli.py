import subprocess
from typing import NoReturn
import click

from src.app.const import APP_CACHE_PATH
from src.app.opener import Cache, get_all_media, get_random_open_cmd
from src.const import PHOTO_PATH, VIDEO_PATH


@click.command()
def pronapp() -> NoReturn:
    cmds_cache = Cache(APP_CACHE_PATH)

    medias = get_all_media(video_path=VIDEO_PATH, photo_path=PHOTO_PATH)
    while True:
        click.confirm(text="Press anything to open the next sauce", show_default=False)
        cmd = get_random_open_cmd(medias=medias, cmds_cache=cmds_cache)
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    pronapp()
