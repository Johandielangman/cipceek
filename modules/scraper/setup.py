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

import os
import re
import argparse
import tomllib
import pathlib

# =============== // CUSTOM IMPORTS // ===============

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# =============== // MODULE IMPORTS // ===============

import modules.utils as utils
import constants as c
import modules.scraper.structures as dc
utils.setup_logger(logger)

# =============== // SERVICE CLASS   // ===============


class Setup:
    args: argparse.Namespace = ...
    config: dc.Config = ...

    def get_chrome_version(self):
        # Thanks, some guy on the internet!
        try:
            if os.name == 'nt':  # Windows
                stream = os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version')
                output = stream.read()
                version_match = re.search(r"version\s+REG_SZ\s+([\d.]+)", output)
                if version_match:
                    return version_match.group(1)
        except Exception as e:
            logger.error(f"Failed to get Chrome version: {e}")
        return None

    def get_service(self) -> ChromeService:
        try:
            chrome_version = self.get_chrome_version()
            logger.debug(f"Chrome version: {chrome_version}")
            exe_path = ChromeDriverManager(driver_version=chrome_version).install()
            logger.debug(f"Using ChromeDriver from: {exe_path}")
            service = ChromeService(executable_path=exe_path)
        except WebDriverException as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            service = None
        except Exception as e:
            logger.error(f"An unexpected error occurred while initializing ChromeDriver: {e}")
            service = None

        if service is None:
            logger.info("Using default ChromeDriver path")
            service = ChromeService()
        else:
            logger.debug(f"Using the driver from: {service.path}")

        return service

    def get_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.config.settings.user_agent}')
        options.add_argument('--log-level=3')
        options.add_argument("--headless=new")
        options.add_experimental_option(
            "prefs", {
                "download.default_directory": str(self.args.root_directory / self.args.tag),
                "savefile.default_directory": str(self.args.root_directory / self.args.tag)
            }
        )
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options

    def load_config(self) -> dc.Config:
        config_path: pathlib.Path = pathlib.Path(c.CONFIG_DIR) / f"{self.args.intellectual_property}.toml"
        data: dict = tomllib.loads(config_path.read_text())
        return dc.Config(**data)
