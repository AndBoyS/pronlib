from pathlib import Path
import subprocess

from natsort import natsorted

from pronlib.folder_index import MediaChapter, PhotoChapter, VideoChapter, get_subfolders, reindex_folders, save_sauce


def main() -> None:
    repo_dir = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
    media_dir = repo_dir.parent / "Test"

    sauce_save_path = repo_dir / "sauce.json"

    video_path = media_dir / "Videos"
    photo_path = media_dir / "Photos"

    video_folders = natsorted(get_subfolders(video_path))
    num_videos = len(video_folders)
    photo_folders = natsorted(get_subfolders(photo_path))
    
    video_chapters: list[MediaChapter] = [VideoChapter(path, i) for i, path in enumerate(video_folders, start=1)]
    photo_chapters: list[MediaChapter] = [
        PhotoChapter(path, i) for i, path in enumerate(photo_folders, start=num_videos + 1)
    ]

    reindex_folders(video_chapters)
    reindex_folders(photo_chapters)
    
    save_sauce(
        video_chapters + photo_chapters,
        save_path=sauce_save_path,
    )


if __name__ == "__main__":
    main()
