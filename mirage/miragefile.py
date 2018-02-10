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
import yaml
from mirage.command import log, raise_error_message


class MiragefileDataCategory(enum.Enum):
    project_name = 0
    project_version = 1
    project_author = 2
    project_git = 3
    project_license = 4
    project_description = 5
    django_path = 6
    django_package_manager = 7
    django_db_backend = 8
    front_path = 9
    front_package = 10
    front_builder = 11
    workspace_path = 12
    copyright_start_year = 13
    copyright_copyrigtors = 14


def get_project(item):
    
    data = load_miragefile()

    if item == MiragefileDataCategory.project_name:
        return data["project"]["name"]
    elif item == MiragefileDataCategory.project_version:
        return data["project"]["version"]
    elif item == MiragefileDataCategory.project_author:
        return data["project"]["author"]
    elif item == MiragefileDataCategory.project_git:
        return data["project"]["git"]
    elif item == MiragefileDataCategory.project_license:
        return data["project"]["license"]
    elif item == MiragefileDataCategory.project_description:
        return data["project"]["description"]
    else:
        log("The config information named " + item + " does not exist!", withError = True) 
        return load_failed()


def get_copyright(item):

    data = load_miragefile()

    if item == MiragefileDataCategory.copyright_start_year:
        return data["project"]["copyright"]["start_year"]
    elif item == MiragefileDataCategory.copyright_copyrigtors:
        return data["project"]["copyright"]["copyrightors"]
    else:
        log("The config information named " + item + " does not exist!", withError = True) 
        return load_failed()


def load_miragefile():
    return _load_yaml("Miragefile")


def load_miragefile_addon():
    return _load_yaml("Miragefile.addon")


def load_miragefile_secret():
    return _load_yaml("Miragefile.secret")

def _load_yaml(filename):
    with open(filename, "r") as yamlfile:
        try: 
            return yaml.load(yamlfile)
        except:
            log("Failed to load Miragefile!", withError = True, errorDetail = raise_error_message(_load_yaml))
            return "Invalid Miragefile"

def load_failed():
    return "Invalid Miragefile"
