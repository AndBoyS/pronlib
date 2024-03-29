from pathlib import Path

from natsort import natsorted
from pronlib.constants import DEBUG, PHOTO_PATH, SAUCE_PATH, VIDEO_PATH

from pronlib.folder_index import MediaChapter, PhotoChapter, VideoChapter, get_subfolders, reindex_folders, get_sauce
from pronlib.utils import dump_json


def main(video_path: Path, photo_path: Path, sauce_save_path: Path | None = None) -> dict[str, int | None]:
    video_folders = natsorted(get_subfolders(video_path))
    photo_folders = natsorted(get_subfolders(photo_path))

    video_chapters: list[MediaChapter] = [VideoChapter(path) for path in video_folders]
    photo_chapters: list[MediaChapter] = [PhotoChapter(path) for path in photo_folders]

    reindex_folders(video_chapters)
    reindex_folders(photo_chapters)

    sauce = get_sauce(video_chapters + photo_chapters)

    if sauce_save_path is not None:
        dump_json(sauce, sauce_save_path)

    return sauce


if __name__ == "__main__":
    if DEBUG:
        print("Warning: script is run in debug mode, to change that, use DEBUG var from pronlib.costants")
    main(video_path=VIDEO_PATH, photo_path=PHOTO_PATH, sauce_save_path=SAUCE_PATH)
