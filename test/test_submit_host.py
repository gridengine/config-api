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
from nose import SkipTest

from .utils import needs_uge
from .utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_list_shosts():
    try:
        hl = API.list_shosts()
        assert (hl is not None)
    except ObjectNotFound as ex:
        raise SkipTest('There are no configured UGE submit hosts.')


def test_object_already_exists():
    try:
        try:
            hl = API.list_shosts()
            if len(hl):
                API.add_shosts([hl[0]])
                assert (False)
            else:
                raise SkipTest('There are no configured UGE submit hosts.')
        except ObjectNotFound as ex:
            raise SkipTest('There are no configured UGE submit hosts.')
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_delete_and_add_shosts():
    try:
        hl = API.list_shosts()
        if not len(hl):
            raise SkipTest('There are no configured UGE submit hosts.')
        host_name = hl[0]
        hl2 = API.delete_shosts([host_name])
        assert (hl2.data.count(host_name) == 0)
        hl3 = API.add_shosts(host_name)
        assert (hl3.data.count(host_name) == 1)
    except ObjectNotFound as ex:
        raise SkipTest('There are no configured UGE submit hosts.')
