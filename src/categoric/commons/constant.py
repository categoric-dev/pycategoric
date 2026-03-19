"""Global constants."""

import getpass
import pathlib
from importlib.resources import files

ETC_DIR = files("categoric").joinpath("etc")
WORK_DIR = pathlib.Path(f"/var/tmp/{getpass.getuser()}")
CACHE_DIR = WORK_DIR.joinpath(".cache")

# Default hosts
DEFAULT_HOST = "0.0.0.0"
LOCALHOST = "127.0.0.1"

# LLM Configuration
DEFAULT_LLM_ENDPOINT = "http://localhost:1234/v1"
