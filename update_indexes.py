from pathlib import Path

from src.const import DEBUG, PHOTO_PATH, SAUCE_PATH, VIDEO_PATH

from src.media_indexing.folder_index import (
    get_chapters,
    reindex_folders,
    get_sauce,
)
from src.utils import dump_json


def main(video_path: Path, photo_path: Path, sauce_save_path: Path | None = None) -> dict[str, int | None]:
    video_chapters, photo_chapters = get_chapters(video_path, photo_path)

    reindex_folders(video_chapters)
    reindex_folders(photo_chapters)

    chapters = video_chapters + photo_chapters
    sauce = get_sauce(chapters)

    if sauce_save_path is not None:
        dump_json(sauce, sauce_save_path)

    return sauce


if __name__ == "__main__":
    if DEBUG:
        print("Warning: script is run in debug mode, to change that, use DEBUG var from pronlib.costants")
    main(video_path=VIDEO_PATH, photo_path=PHOTO_PATH, sauce_save_path=SAUCE_PATH)
