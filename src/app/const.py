from pathlib import Path


OPEN_VIDEO_CMD = 'iina "{path}"'
OPEN_PHOTO_CMD = 'open -a "/Applications/ACDSee Photo Studio 8.app" "{path}"'

APP_CACHE_PATH = Path(__file__).parent / ".app_cache.pkl"
DEBUG_CACHE_PATH = Path(__file__).parent / ".app_cache_debug.pkl"
