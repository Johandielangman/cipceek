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
import datetime

# =============== // CUSTOM IMPORTS // ===============

import modules as m
from loguru import logger
from version.version import __version__
import constants as c
import os

# =============== // PRE SETUP // ===============

__file: pathlib.Path = pathlib.Path(__file__)
m.utils.setup_logger(logger)


# =============== // MAIN FUNCTION AND EXECUTION // ===============

if __name__ == "__main__":
    args: argparse.Namespace = m.parse_args(
        file_name=__file.name,
        version=__version__
    )
    logger.info(f"Logs will be saved to {c.LOG_DIR}")
    logger.info(f"Run is tagged with {args.tag}")

    # =============== // QUICK VALIDATION // ===============

    if os.name != 'nt':
        logger.error("This application can only run in Windows")
        exit(1)

    if (
        len(args.years) == 1 and
        args.years[0] == 0
    ):
        args.years = list(range(1955, datetime.datetime.now().year + 1))

    # =============== // DETERMINE WHAT TO RUN // ===============

    match args.command:
        case "scrape":
            logger.info("Starting scrape")
            m.utils.scrape_pre_heat(args)
            with m.Scraper(args) as s:
                s.run_flow()
