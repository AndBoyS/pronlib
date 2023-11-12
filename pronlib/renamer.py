from __future__ import annotations


from pathlib import Path
import re

from natsort import natsorted


def get_subfolders(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.is_dir() and p.name.lower() != ".ds_store"]


def get_content_subfiles(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.name.lower() not in [".ds_store", "meta.json"]]


class FolderIndexer:
    def reindex_folders(self, base_path: Path, depth: int = 1, start_index: int = 1) -> None:
        subfiles = natsorted(get_subfolders(base_path))
        rename_mapping: dict[Path, Path] = {}

        for i, subfile in enumerate(subfiles, start=start_index):
            if depth > 1:
                self.reindex_folders(subfile, depth=depth - 1)

            stem = subfile.stem.replace('_temp', '')
            stem = re.sub(r"^\d+", "", stem).strip()

            counter_ptrn = re.compile(r"\(\d+\)$")
            counter_match = counter_ptrn.search(stem)

            if counter_match is None:
                artist_ptrn = re.compile(r"\[.+\]$")
                artist_match = artist_ptrn.search(stem)
                name_ending = ""
                if artist_match is not None:
                    stem = artist_ptrn.sub("", stem).strip()
                    name_ending = artist_match.group().title()

            else:
                if not subfile.is_dir():
                    raise ValueError(f"{subfile} is not a dir, but its expected to be")
                stem = counter_ptrn.sub("", stem).strip()
                name_ending = f"({len(get_content_subfiles(subfile))})"

            new_stem = f"{i} {stem} {name_ending}".strip()
            new_name = f"{new_stem}{subfile.suffix}"

            new_subfile = subfile.with_name(new_name)
            temp_name = f'{subfile.stem}_temp{subfile.suffix}'
            subfile = subfile.rename(subfile.with_name(temp_name))
            rename_mapping[subfile] = new_subfile

        for path, new_path in rename_mapping.items():
            path.rename(new_path)
