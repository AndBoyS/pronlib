from pathlib import Path

from pronlib.update_files import PhotoUpdater, VideoUpdater
from pronlib.update_meta import update_meta_files, update_random_file


def main():
    base_dir = Path().resolve().parent
    photos_dir = base_dir / 'Photos'
    videos_dir = base_dir / 'Videos'

    photo_updater = PhotoUpdater(photos_dir)
    video_updater = VideoUpdater(videos_dir, photos_dir)

    photo_updater.update()
    video_updater.update()

    update_random_file(photos_dir, videos_dir)
    update_meta_files(photos_dir)


if __name__ == '__main__':
    main()
