from src.const import PHOTO_PATH, VIDEO_PATH
from src.media_indexing.folder_index import get_chapters


def main() -> None:
    _, photo_chapters = get_chapters(VIDEO_PATH, PHOTO_PATH)

    artists: set[str] = set()

    for chapter in photo_chapters:
        for media in chapter.media_list:
            if media.artist_name is not None:
                artists.add(media.artist_name)

    print(*artists, sep="\n")


if __name__ == "__main__":
    main()
