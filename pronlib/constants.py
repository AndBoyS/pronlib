from pathlib import Path
import subprocess


REPO_PATH = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
VIDEO_PATH = REPO_PATH.parent / "[Content]/Videos"
PHOTO_PATH = REPO_PATH.parent / "[Content]/Photos"
SAUCE_PATH = REPO_PATH / "sauce.json"
META_NAME = "meta.json"
