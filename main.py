from pathlib import Path

from pronlib.renamer import FolderIndexer, get_subfolders


def main() -> None:
    root_path = Path(__file__).parents[1] / "Test"

    folder_renamer = FolderIndexer()

    videos_path = root_path / "Videos"
    photos_path = root_path / "Photos"

    num_video_folders = len(get_subfolders(videos_path))

    folder_renamer.reindex_folders(
        videos_path,
        depth=1,
    )

    folder_renamer.reindex_folders(
        photos_path,
        depth=2,
        start_index=num_video_folders + 1,
    )


if __name__ == "__main__":
    main()
