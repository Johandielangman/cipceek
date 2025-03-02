# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: March 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import argparse
import pathlib

# =============== // VERSION IMPORT // ===============

from version import __version__


# =============== // FILE PATH PROCESSING // ===============

__file = pathlib.Path(__file__)

FILE_NAME: str = __file.name
ROOT_DIR: pathlib.Path = __file.resolve().parent
VERSION_FILE_PATH: pathlib.Path = ROOT_DIR / "version.py"


if __name__ == "__main__":
    # =============== // ARGPARSE // ===============

    parser = argparse.ArgumentParser(
        prog=FILE_NAME,
        description='Bump the version'
    )
    parser.add_argument(
        "--major",
        action="store_true",
        help="Bump the major version"
    )
    parser.add_argument(
        "--minor",
        action="store_true",
        help="Bump the minor version"
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        help="Bump the patch version"
    )
    args = parser.parse_args()
    if not any([args.major, args.minor, args.patch]):
        parser.error("No version bump type provided")

    # =============== // VERSION BUMP // ===============

    major, minor, patch = [int(v) for v in __version__.split(".")]
    if args.major:
        major += 1
        minor = 0
        patch = 0
    elif args.minor:
        minor += 1
        patch = 0
    elif args.patch:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    # =============== // FILE WRITE // ===============

    print(f"Bumping version from {__version__} to {new_version}")
    VERSION_FILE_PATH.write_text(f'__version__ = "{new_version}"\n')
