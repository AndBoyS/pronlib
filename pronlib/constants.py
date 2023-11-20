from pathlib import Path
import subprocess


DEBUG = True
REPO_PATH = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())

if DEBUG:
    MEDIA_PATH = REPO_PATH / "tests/test_media"
else:
    MEDIA_PATH = REPO_PATH.parent / "[Content]"

VIDEO_PATH = MEDIA_PATH / "Videos"
PHOTO_PATH = MEDIA_PATH / "Photos"
SAUCE_PATH = REPO_PATH / "sauce.json"
META_NAME = "meta.json"
