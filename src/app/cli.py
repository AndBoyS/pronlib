import subprocess
import click

from src.app.const import APP_CACHE_PATH
from src.app.opener import Cache, get_all_media, get_random_media
from src.const import PHOTO_PATH, VIDEO_PATH


@click.command()
@click.option("--no-reset", "is_reset", flag_value=False, default=True, help="Don't reset the cache (default)")
@click.option("--reset", "is_reset", flag_value=True, help="Reset the cache")
def pronapp(is_reset: bool) -> None:
    if is_reset:
        APP_CACHE_PATH.unlink(missing_ok=True)
        return

    media_cache = Cache(APP_CACHE_PATH)

    medias = get_all_media(video_path=VIDEO_PATH, photo_path=PHOTO_PATH)
    while True:
        click.confirm(text="Press anything to open the next sauce", show_default=False)
        media = get_random_media(medias=medias, media_cache=media_cache)
        click.echo(f"{media.title} ({len(media_cache)}/{len(medias)})")
        subprocess.call(media.open_cmd, shell=True)


if __name__ == "__main__":
    pronapp()
