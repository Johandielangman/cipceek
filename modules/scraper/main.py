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

import time
import argparse
from types import TracebackType
from typing import (
    Optional,
    Type
)

# =============== // CUSTOM IMPORTS // ===============

from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# =============== // MODULE IMPORTS // ===============

from modules.scraper.setup import Setup
import modules.scraper.structures as dc
import modules.utils as utils
import constants as c
from modules.scraper.flows import (
    WebDriverFlows
)

utils.setup_logger(logger)

# =============== // PRIMARY SCRAPER // ===============


class Scraper(
    Setup,
    WebDriverFlows
):
    def __init__(
        self,
        args: argparse.Namespace
    ) -> None:
        logger.debug("Initializing scraper...")
        self.args: argparse.Namespace = args
        self.config: dc.Config = self.load_config()

        service: ChromeService = self.get_service()
        options: webdriver.ChromeOptions = self.get_options()

        try:
            webdriver.Chrome.__init__(
                self,
                service=service,
                options=options
            )
        except Exception as e:
            logger.error(f"An error has occurred while initializing Chrome: {e}")
            logger.info(f"Trying again with the executable path: {c.ROOT_DIR}")
            service: ChromeService = ChromeService(
                executable_path=str(c.ROOT_DIR / "chromedriver.exe")
            )
            try:
                webdriver.Chrome.__init__(self, service=service, options=options)
            except Exception as e:
                logger.error(f"An error has occurred while initializing Chrome: {e}")
                raise e

        self.implicitly_wait(self.config.settings.implicit_wait_sec)
        self.explicit_wait_timeout = self.config.settings.explicit_wait_sec
        logger.info("Scraper successfully initialized")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        if exc_type is not None:
            logger.error(f"An error has occurred: {exc_type}: {exc_val}")
        logger.info("Tearing down scraper")
        self.quit()

    def run_flow(
        self
    ) -> None:
        self.login()
        self.go_to_advanced()
        self.download_excel()
        time.sleep(30)
        return
