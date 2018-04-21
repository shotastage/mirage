# -*- coding: utf-8 -*-
"""
Copyright 2017-2018 Shota Shimazu.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
import enum
import json
import pathlib
from mirage import system as mys
from mirage.proj import MirageEnvironment, MirageEnvironmentLevel, Detail
from mirage.exceptions import MiragefileUnknownError
from functools import lru_cache


class Category(enum.Enum):
    ProjectBasic    = 0
    DjangoProject   = 1
    FrontProject    = 2
    Copyright       = 3





class MirageFormat(enum.Enum):
    yaml = 0
    json = 1
    python = 2


class Config():

    def __init__(self):
        self._mirageformat = MirageFormat.python

    def load_miragefile(self):

        with MirageEnvironment(MirageEnvironmentLevel.inproject):
            pass



class A_Config():

    def __init__(self, file_type = None):

        with MirageEnvironment(MirageEnvironmentLevel.inproject):
            if file_type == "secret":
                self._data = self._load_json("Miragefile.secret")
            elif file_type == "addon":
                self._data = self._load_json("Miragefile.addon")
            elif file_type == None:
                self._data = self._load_json("Miragefile")
            else:
                mys.log("Wrong configuration type {0}.".format(file_type), withError = True)


    @lru_cache(maxsize = 100)
    def get(self, category, detail):

        try:
            if category == Category.project_basic:
                return self._get_project(detail)
            if category == Category.django:
                return self._get_django(detail)
            if category == Category.copyright:
                return self._get_copyright(detail)
            if category == Category.private_profile:
                return self._get_private_profile(detail)
        except:
            mys.log("Failed to get value from Miragefile!", withError = True)


    @lru_cache(maxsize = 100)
    def _get_project(self, detail):

        if detail == Detail.project_name:
            return self._data["project"]["name"]
        elif detail == Detail.project_version:
            return self._data["project"]["version"]
        elif detail == Detail.project_author:
            return self._data["project"]["author"]
        elif detail == Detail.project_git:
            return self._data["project"]["git"]
        elif detail == Detail.project_license:
            return self._data["project"]["license"]
        elif detail == Detail.project_description:
            return self._data["project"]["description"]
        else:
            mys.log("The config information named " + str(detail) + " does not exist!", withError = True) 
            raise MiragefileUnknownError


    @lru_cache(maxsize = 100)
    def _get_django(self, detail):

        if detail == Detail.django_path:
            return self._data["project"]["django"]["path"]
        elif detail == Detail.django_module:
            return self._data["project"]["django"]["module"]
        elif detail == Detail.django_package_manager:
            return self._data["project"]["django"]["package"]
        elif detail == Detail.django_db_backend:
            return self._data["project"]["django"]["database"]
        else:
            mys.log("The config information named " + str(detail) + " does not exist!", withError = True) 
            raise MiragefileUnknownError


    @lru_cache(maxsize = 100)
    def _get_copyright(self, detail):

        if detail == Detail.copyright_start_year:
            return self._data["project"]["copyright"]["start_year"]
        elif detail == Detail.copyright_copyrigtors:
            return self._data["project"]["copyright"]["copyrightors"]
        else:
            mys.log("The config information named " + detail + " does not exist!", withError = True) 
            raise MiragefileUnknownError


    @lru_cache(maxsize = 100)
    def _get_private_profile(self, detail):

        if detail == Detail.private_name:
            return self._data["private_profile"]["name"]
        elif detail == Detail.private_license_url:
            return self._data["private_license"]["url"]
        else:
            mys.log("The config information named " + detail + " does not exist!", withError = True) 
            raise MiragefileUnknownError


    @lru_cache(maxsize = 100)
    def _load_json(self, filename):
        if not os.path.exists(filename):
            mys.log("Failed to find Miragefile!", withError = True)
            raise FileNotFoundError

        with open(filename, "r") as jsonfile:
            try:
                return json.load(jsonfile)
            except:
                mys.log("Failed to load Miragefile!", withError = True, errorDetail = mys.raise_error_message(self._load_json))
                raise FileNotFoundError