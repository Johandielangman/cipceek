# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: March 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

import pathlib
import tempfile

__file: pathlib.Path = pathlib.Path(__file__)

# =============== // PROJECT DIRECTORY // ===============

ROOT_DIR: pathlib.Path = __file.resolve().parent
STATIC_DIR: pathlib.Path = ROOT_DIR / "static"
CONFIG_DIR: pathlib.Path = ROOT_DIR / "config"

# =============== // TEMP DIRECTORY // ===============

TEMP_DIR: pathlib.Path = pathlib.Path(tempfile.gettempdir()) / "cipceek"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR: pathlib.Path = TEMP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_LOGS_DIR: pathlib.Path = LOG_DIR / "debug"
ERROR_LOGS_DIR: pathlib.Path = LOG_DIR / "errors"
