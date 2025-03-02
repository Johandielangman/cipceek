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

from typing import (
    List
)

# =============== // CUSTOM IMPORTS // ===============

from pydantic import (
    BaseModel,
    PositiveInt
)

# =============== // DATA CLASSES // ===============


class Links(BaseModel):
    root: str
    login_path: str
    home_path: str
    patent_search_path: str


class Settings(BaseModel):
    implicit_wait_sec: PositiveInt
    explicit_wait_sec: PositiveInt
    user_agent: str


class LoginLookup(BaseModel):
    username_input: List[str]
    password_input: List[str]
    login_button: List[str]


class AdvancedSearchLookup(BaseModel):
    simple_search_button: List[str]
    advanced_search_button: List[str]
    application_from_input: List[str]
    application_to_input: List[str]
    column_checkboxes: List[str]
    search_button: List[str]


class SimpleSearchLookup(BaseModel):
    simple_search_button: List[str]
    advanced_search_button: List[str]
    application_number_input: List[str]
    search_button: List[str]


class SearchLookup(BaseModel):
    simple: SimpleSearchLookup
    advanced: AdvancedSearchLookup


class ResultsLookup(BaseModel):
    print_mode_select: List[str]
    print_list_button: List[str]


class Lookup(BaseModel):
    login: LoginLookup
    search: SearchLookup
    results: ResultsLookup


class Config(BaseModel):
    title: str
    links: Links
    lookup: Lookup
    settings: Settings
