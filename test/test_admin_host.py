#!/usr/bin/env python
# 
#___INFO__MARK_BEGIN__ 
########################################################################## 
# Copyright 2016,2017 Univa Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
########################################################################### 
#___INFO__MARK_END__ 
# 
from nose import SkipTest

from .utils import needs_uge
from .utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.authorization_error import AuthorizationError

create_config_file()
API = QconfApi()
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()

@needs_uge
def test_list_ahosts():
    try:
        hl = API.list_ahosts()
        assert(hl is not None)
    except ObjectNotFound as ex:
        raise SkipTest('There are no configured UGE admin hosts.')


def test_object_already_exists():
    try:
        try:
            hl = API.list_ahosts()
            API.add_ahosts([hl[0]])
            assert(False)
        except ObjectNotFound as ex:
            raise SkipTest('There are no configured UGE admin hosts.')
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_delete_and_add_ahosts():
    try:
        hl = API.list_ahosts()
        host_name = None
        for h in hl:
            if h != CONFIG_MANAGER['host']:
                host_name = h
                break
        if not host_name:
            raise SkipTest('Could not find UGE admin host that could be removed.')
        try:
            hl2 = API.delete_ahosts([host_name])
            assert(hl2.data.count(host_name) == 0)
        except AuthorizationError as ex:
            raise SkipTest('Skip master host warning %s.' % str(ex))
        hl3 = API.add_ahosts(host_name)
        assert(hl3.data.count(host_name) == 1)
    except ObjectNotFound as ex:
        raise SkipTest('There are no configured UGE admin hosts.')
