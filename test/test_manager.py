#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2016-2021 Univa Corporation (acquired and owned by Altair Engineering Inc.)
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#######################################################################################
# ___INFO__MARK_END__
# 
from .utils import needs_uge
from .utils import create_config_file
from .utils import generate_random_string

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
MANAGER_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_list_managers():
    ol = API.list_managers()
    assert (ol is not None)


def test_add_manager():
    ol = API.list_managers()
    ol2 = API.add_managers([MANAGER_NAME])
    assert (len(ol2) == len(ol) + 1)
    assert (ol2.count(MANAGER_NAME) == 1)


def test_delete_manager():
    ol = API.list_managers()
    ol2 = API.delete_managers([MANAGER_NAME])
    assert (len(ol2) == len(ol) - 1)
    assert (ol2.count(MANAGER_NAME) == 0)


def test_object_already_exists():
    API.add_managers([MANAGER_NAME])
    try:
        API.add_managers([MANAGER_NAME])
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass
    API.delete_managers([MANAGER_NAME])


def test_object_not_found():
    try:
        API.delete_managers([MANAGER_NAME])
    except ObjectNotFound as ex:
        # ok
        pass
