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
import uuid
import shutil
import sqlite3
import contextlib
from mirage import fileable
from mirage import system as mys
from mirage.proj import MirageEvironmet, MirageEvironmetLevel


class MirageWorkspace():

    @staticmethod
    def initialize():

        with MirageEvironmet(MirageEvironmetLevel.inproject):
            if not fileable.exists(".mirage"):
                mys.log("Creating Mirage workspace...")
                fileable.mkdir(".mirage")
                fileable.mkdir(".mirage/cache/")
                fileable.mkdir(".mirage/persistence/")


    @staticmethod
    def persist(file_path, domain):
        object_id = str(uuid.uuid4())
        absolute_path = os.getcwd() + "/" + file_path

        with MirageEvironmet(MirageEvironmetLevel.inproject):

            mys.log("Safety caching...")
            fileable.cd(".mirage/cache/")
            fileable.copy(absolute_path, os.getcwd() + "/" + file_path, force = True)

            mys.log("Archiving files...")
            shutil.make_archive(object_id, "zip", root_dir = absolute_path)
            
            fileable.move(object_id + ".zip", "../persistence/")

            MirageWorkspace.__write_persistence_file_meta(object_id, ".mirage/persistence/", domain)
            

    @staticmethod
    def cache(file):
        pass

    @staticmethod
    def __write_persistence_file_meta(object_id, path, domain):
        con = sqlite3.connect(MirageWorkspace.__db_connect())
        cur = con.cursor()

        MirageWorkspace.query_execute(con, cur,
            "CREATE TABLE IF NOT EXISTS mi_ws_persistences (uuid TEXT PRIMARY KEY, path TEXT, domain TEXT);")

        MirageWorkspace.query_execute(con, cur,
            "INSERT INTO mi_ws_persistences VALUES (\"{0}\", \"{1}\", \"{2}\");".format(object_id, path, domain))
        con.commit()
        con.close()


    @staticmethod
    def __db_connect():
        return MirageEvironmet.search_project_root() + "/.mirage/mirage_workspace.sqlite3"


    @staticmethod
    def query_execute(connection, cur, query):
        try:
            cur.execute(query)
        except sqlite3.Error as e:
            mys.log("SQLite3 error has occured!", withError = True, errorDetail = e.args[0])
        except:
            mys.log("Unknown error has occured!", withError = True,
                            errorDetail = mys.raise_error_message(MirageWorkspace.__write_persistence_file_meta))
