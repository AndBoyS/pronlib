from pathlib import Path
import shutil
from typing import Iterator

import pytest
from main import main

expected_sauce = {"1 Eroge!": 3, "2 Honoo no Oppai": 4, "3 Honoo Haramase Appli": 5, "4 M1": 6}

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
    "3 Honoo Haramase Appli (5)",
    "4 M1 (6)",
    "1",
    "4",
    "3",
    "2",
    "5",
    "meta.json",
    "3 Ikinari Kozukuri [Goban]",
    "2 Scarlet princess Rias Daisuki [Izumi Mahiru]",
    "4 Hokorashiki Goshujin-sama [Morimoto Seina, Crowly]",
    "1 Maoo Wonderful [Izumi Mahiru]",
    "5 Gimme Attention! Doggy x2 Girls [Minamino Sazan]",
    "6 Blossoming Sakura! [Kakao]",
]


@pytest.fixture
def test_data_dir() -> Iterator[Path]:
    media_dir_original = Path(__file__).parent / "test_media"
    media_dir = Path(__file__).parent / "test_media_copy"
    shutil.copytree(media_dir_original, media_dir)
    yield media_dir
    shutil.rmtree(media_dir)


def test_rename_and_sauce(test_data_dir: Path) -> None:
    sauce = main(test_data_dir)
    assert sauce == expected_sauce
    media_names = [p.name for p in test_data_dir.rglob("*") if not p.name.startswith(".")]
    assert set(expected_media_names) == set(media_names)
