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
import os
import pathlib

# =============== // MODULE IMPORTS // ===============

import constants as c

# =============== // UTILS // ===============


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
    parser.add_argument(
        '-c',
        '--config',
        help='Path to the scraper.toml config file',
        type=pathlib.Path,
        default=(c.CONFIG_DIR / "default.toml")
    )
    parser.set_defaults(command='scrape')
