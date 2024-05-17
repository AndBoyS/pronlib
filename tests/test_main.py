from pathlib import Path
import shutil
from typing import Iterator

import pytest
from update_indexes import main

expected_sauce = {"Eroge!": 3, "Honoo no Oppai": 4, "Honoo Haramase Appli": 5, "M1": 6}

expected_media_names = [
    "Videos",
    "Photos",
    "1 Eroge! (3)",
    "2 Honoo no Oppai (4)",
    "3 Eroge - 3.mp4",
    "2 Eroge - 2.mp4",
    "1 Eroge - 1.mp4",
    "1 Chichiiro Toiki - 1.mp4",
    "2 Honoo no Haramase Oppai Ero Appli Gakuen - 01.mp4",
    "3 Honoo no Haramase Oppai Ero Appli Gakuen - 02.mp4",
    "4 Joshi-ochi.mp4",
    "1 Honoo Haramase Appli (5)",
    "2 M1 (6)",
    "1",
    "horny_photo.txt",
    "4",
    "horny_photo.txt",
    "3",
    "horny_photo.txt",
    "2",
    "horny_photo.txt",
    "5",
    "horny_photo.txt",
    "3 Ikinari Kozukuri [Goban]",
    "horny_photo.txt",
    "2 Scarlet princess Rias Daisuki [Izumi Mahiru]",
    "horny_photo.txt",
    "4 Hokorashiki Goshujin-sama [Morimoto Seina, Crowly]",
    "horny_photo.txt",
    "1 Maoo Wonderful [Izumi Mahiru]",
    "horny_photo.txt",
    "5 Gimme Attention! Doggy x2 Girls [Minamino Sazan]",
    "horny_photo.txt",
    "6 Blossoming Sakura! [Kakao]",
    "horny_photo.txt",
]


@pytest.fixture
def video_and_photo_paths() -> Iterator[tuple[Path, Path]]:
    media_dir_original = Path(__file__).parent / "test_media"
    media_dir = media_dir_original.with_name("test_media_copy")
    shutil.copytree(media_dir_original, media_dir)
    yield media_dir / "Videos", media_dir / "Photos"
    shutil.rmtree(media_dir)


def test_rename_and_sauce(video_and_photo_paths: tuple[Path, Path]) -> None:
    video_path, photo_path = video_and_photo_paths
    media_path = video_path.parent

    assert video_path.parent == photo_path.parent, "Same parent for video and photo expected"
    sauce = main(video_path=video_path, photo_path=photo_path)
    assert sauce == expected_sauce
    media_names = [p.name for p in media_path.rglob("*") if not p.name.startswith(".")]
    assert sorted(expected_media_names) == sorted(media_names)
