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

import argparse
import pathlib
import time
import os

# =============== // CUSTOM IMPORTS // ===============

from ulid import ULID

# =============== // MODULE IMPORTS // ===============

import constants as c

# =============== // UTILS // ===============


def get_ulid() -> str:
    return str(ULID.from_timestamp(time.time()))


def get_banner(
    dir: pathlib.Path = c.STATIC_DIR / "banner.txt"
) -> str:
    return dir.read_text()

# =============== // PRIMARY PARSER // ===============


def parse_args(
    file_name: str,
    version: str
) -> argparse.Namespace:
    # =============== // BASIC SETUP // ===============

    parser = argparse.ArgumentParser(
        prog=file_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Welcome to the CIPC Scraper!\n\n"
            f"{get_banner()}"
        ),
        epilog="Epilog..."
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=version)
    )
    subparsers: argparse._SubParsersAction = parser.add_subparsers(
        help='Actions You can Perform'
    )

    # =============== // ADD SUB PARSERS // ===============

    add_scrape_subparser(subparsers)

    return parser.parse_args()

# =============== // SECONDARY (SUB) PARSER // ===============


def add_scrape_subparser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('scrape', help='Start to perform a CIPC scrape')
    parser.add_argument(
        '-i',
        '--intellectual-property',
        choices=["patents"],  # TODO  Trade marks, designs, copyright
        help='Which intellectual property to scrape',
        required=True
    )
    add_cipc_arguments(parser)
    add_folder_arguments(parser)
    parser.set_defaults(command='scrape')


# =============== // GENERAL ARGUMENTS // ===============

def add_cipc_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-u',
        '--username',
        help='CIPC search username',
        type=str,
        default=os.getenv("CIPC_USERNAME")
    )
    parser.add_argument(
        '-p',
        '--password',
        help='CIPC search password',
        type=str,
        default=os.getenv("CIPC_PASSWORD")
    )
    parser.add_argument(
        '-c',
        '--config',
        help='Path to the scraper.toml config file',
        type=pathlib.Path,
        default=(c.CONFIG_DIR / "default.toml")
    )


def add_folder_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-t',
        '--tag',
        help='Give the run a tag name',
        type=str,
        default=get_ulid()
    )
    parser.add_argument(
        '-r',
        '--root-directory',
        help='The root directory where everything is saved',
        type=pathlib.Path,
        default=c.TEMP_DIR
    )
