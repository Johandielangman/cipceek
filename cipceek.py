#! ./.venv/Scripts/python
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: March 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORTS // ===============

import pathlib
import argparse

# =============== // CUSTOM IMPORTS // ===============

import modules as m
from loguru import logger
from version.version import __version__
import constants as c

# =============== // PRE SETUP // ===============

__file: pathlib.Path = pathlib.Path(__file__)
m.setup_logger(logger)


# =============== // MAIN FUNCTION AND EXECUTION // ===============

if __name__ == "__main__":
    args: argparse.Namespace = m.parse_args(
        file_name=__file.name,
        version=__version__
    )
    logger.info(f"Logs will be saved to {c.LOG_DIR}")

    # =============== // DETERMINE WHAT TO RUN // ===============

    match args.command:
        case "scrape":
            logger.info("Starting scrape")
