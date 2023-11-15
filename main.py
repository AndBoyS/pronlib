from pathlib import Path

from pronlib.folder_index import FolderIndexer, get_subfolders


def main() -> None:
    root_path = Path(__file__).parents[1] / "Test"

    folder_indexer = FolderIndexer()

    video_path = root_path / "Videos"
    photo_path = root_path / "Photos"

    num_video_folders = len(get_subfolders(video_path))

    folder_indexer.reindex_video_folders(
        video_path,
    )

    folder_indexer.reindex_photo_folders(
        photo_path,
        start_index=num_video_folders + 1,
    )
    folder_indexer.save_sauce()
    

if __name__ == '__main__':
    main()