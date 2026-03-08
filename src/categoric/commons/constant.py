import getpass
import pathlib
from importlib.resources import files

ETC_DIR = files("categoric").joinpath("etc")
WORK_DIR = pathlib.Path(f"/var/tmp/{getpass.getuser()}")
CACHE_DIR = WORK_DIR.joinpath(".cache")
