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

import datetime
import argparse
import constants as c
from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from loguru import Logger

# =============== // LOGGER SETUP // ===============


def get_today() -> str:
    return datetime.date.today().strftime("%Y_%m_%d")


def setup_logger(logger: 'Logger'):
    debug_logs: str = f"debug_{get_today()}.log"
    warning_logs: str = f"errors_{get_today()}.log"

    logger.add(
        f"{c.DEBUG_LOGS_DIR / debug_logs}",
        level="DEBUG",
        rotation="20 MB",
        retention="7 days",
        compression="zip"
    )

    logger.add(
        f"{c.ERROR_LOGS_DIR / warning_logs}",
        level="WARNING",
        rotation="20 MB",
        retention="30 days",
        compression="zip"
    )


# =============== // ENVIRONMENT SETUP // ===============

def scrape_pre_heat(args: argparse.Namespace) -> None:
    (args.root_directory / args.tag).mkdir(parents=True, exist_ok=False)
    if args.root_directory != c.TEMP_DIR:
        (args.root_directory / args.tag / "logs.txt").write_text(
            "Looking for logs?\n"
            f"Logs are saved to {c.LOG_DIR}"
        )
