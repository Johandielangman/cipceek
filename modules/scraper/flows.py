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
from functools import wraps
from typing import (
    List,
    Callable,
    Any
)

# =============== // CUSTOM IMPORTS // ===============

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from loguru import logger

# =============== // MODULE IMPORTS // ===============

import modules.scraper.structures as dc
from modules.arg_parser import get_ulid
import modules.utils as utils

utils.setup_logger(logger)

# =============== // FOUNDATIONS // ===============


def check_login_url(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: "FlowBase", *args: Any, **kwargs: Any) -> Any:
        self.did_they_kick_me_out_again()
        return func(self, *args, **kwargs)
    return wrapper

# =============== // FOUNDATIONS // ===============


class FlowBase(webdriver.Chrome):
    args: argparse.Namespace = ...
    config: dc.Config = ...

    @property
    def login_link(self) -> str:
        return f"{self.config.links.root}{self.config.links.login_path}"

    @property
    def patent_search_link(self) -> str:
        return f"{self.config.links.root}{self.config.links.patent_search_path}"

    def wait_for_id(
        self,
        id_: str
    ):
        WebDriverWait(
            self,
            self.explicit_wait_timeout
        ).until(
            lambda x: x.find_element(By.ID, id_)
        )

    def did_they_kick_me_out_again(self) -> None:
        if self.current_url == self.login_link:
            logger.warning("Current URL matches login URL. Re-attempting login.")
            self.login()

    def x_find_element(
        self,
        config: List[str]
    ) -> WebElement:
        by, element = config
        return self.find_element(
            getattr(By, by),
            element
        )

    def login(self) -> None:
        logger.debug(f"Logging into {self.login_link}...")

        # ====> (1) NAVIGATE TO LOGIN PAGE
        self.get(self.login_link)

        # ====> (2) WAIT FOR USER INPUT
        self.wait_for_id(self.config.lookup.login.username_input[1])

        # ====> (3) DECLARE ELEMENTS
        username_input: WebElement = self.x_find_element(
            self.config.lookup.login.username_input
        )
        password_input: WebElement = self.x_find_element(
            self.config.lookup.login.password_input
        )

        # ====> (4) CLEAR ANY CURRENT INPUT
        username_input.clear()
        password_input.clear()

        # ====> (5) INPUT CREDENTIALS
        username_input.send_keys(
            self.args.username
        )
        password_input.send_keys(
            self.args.password
        )

        # ====> (6) PRESS THE BIG BUTTON
        self.x_find_element(
            self.config.lookup.login.login_button
        ).click()
        return


class AdvancedPatentSearchFlow(FlowBase):
    @check_login_url
    def advanced_patent_search(self, year: int) -> None:
        logger.debug(f"Navigating to {self.patent_search_link}")

        # ====> (1) NAVIGATE TO PATENT SEARCH
        self.get(self.patent_search_link)

        # ====> (2) AM I WHERE I WANNA BE?
        self.did_they_kick_me_out_again()
        self.wait_for_id(
            self.config.lookup.search.advanced.advanced_search_button[1]
        )

        # ====> (3) GO TO THE ADVANCED SEARCH
        self.x_find_element(
            self.config.lookup.search.advanced.advanced_search_button
        ).click()

        # ====> (4) AM I WHERE I WANNA BE?
        self.did_they_kick_me_out_again()
        self.wait_for_id(
            self.config.lookup.search.advanced.application_from_input[1]
        )

        # ====> (5) INPUT TEXT
        application_from_input: WebElement = self.x_find_element(
            self.config.lookup.search.advanced.application_from_input
        )
        application_from_input.clear()
        application_from_input.send_keys(f"{year}/00001")

        application_to_input: WebElement = self.x_find_element(
            self.config.lookup.search.advanced.application_to_input
        )
        application_to_input.clear()
        application_to_input.send_keys(f"{year + 1}/00001")

        # ====> (6) CHECK ADDITIONAL COLUMNS
        for i in range(9, 18):
            checkbox: WebElement = self.x_find_element([
                self.config.lookup.search.advanced.column_checkboxes[0],
                self.config.lookup.search.advanced.column_checkboxes[1].format(i=i)
            ])
            checkbox.click()

        # ====> (7) AND... GO!
        self.x_find_element(
            self.config.lookup.search.advanced.search_button
        ).click()
        return

    @check_login_url
    def is_patent_search_results(self) -> bool:
        try:
            self.x_find_element(self.config.lookup.results.print_mode_select)
        except NoSuchElementException:
            logger.warning("Hmm... I don't see the results... Is there an error message?")
            try:
                self.x_find_element(self.config.lookup.search.advanced.error_message)
            except NoSuchElementException:
                logger.error("I have no idea where I am! Giving Up!")
                return False
            else:
                return False
        else:
            return True

    @check_login_url
    def download_patent_excel(self, year: int):
        logger.debug("Downloading Excel File")
        downloads_directory: pathlib.Path = self.args.root_directory / self.args.tag
        excel_file_name: str = f"{self.args.intellectual_property}_{year}.xls"

        # ====> (1) AM I WHERE I WANNA BE?
        self.wait_for_id(
            self.config.lookup.results.print_list_button[1]
        )

        # ====> (2) SELECT EXCEL FORMAT
        Select(
            self.x_find_element(self.config.lookup.results.print_mode_select)
        ).select_by_visible_text("Excel")

        # ====> (3) GET THE DOWNLOADS BEFORE WE DOWNLOAD
        files: List[str] = [
            f.name for f in downloads_directory.iterdir()
        ]

        # ====> (4) FIND AND PRESS THE DOWNLOAD BUTTON
        self.x_find_element(
            self.config.lookup.results.print_list_button
        ).click()

        # ====> (5) WAIT FOR THE DOWNLOAD TO FINISH
        for _ in range(50):
            if any(
                ".crdownload" in f.name
                for f in downloads_directory.iterdir()
            ):
                break
            else:
                time.sleep(0.2)

        for _ in range(3):
            if any(
                ".crdownload" in f.name
                for f in downloads_directory.iterdir()
            ):
                time.sleep(5)
            else:
                break

        # ====> (6) GET THE FILES AFTER THE DOWNLOAD - the new one is the one we want to rename
        new_files: List[str] = [
            f.name for f in downloads_directory.iterdir()
        ]
        file_diff: str = list(set(new_files) - set(files))
        if not file_diff:
            logger.warning("Nothing downloaded!")
            self.save_screenshot(downloads_directory / f"nothing_downloaded_{get_ulid()}.png")
            return
        new_file = file_diff[0]
        (downloads_directory / new_file).rename(
            downloads_directory / excel_file_name
        )


class WebDriverFlows(
    AdvancedPatentSearchFlow
):
    ...
