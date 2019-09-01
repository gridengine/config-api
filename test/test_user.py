#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__
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
# ___INFO__MARK_END__
# 
import types
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
USER_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_object_not_found():
    try:
        user = API.get_user('__non_existent_user__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_user():
    user = API.generate_user(USER_NAME)
    assert (user.data['name'] == USER_NAME)


def test_add_user():
    try:
        userl = API.list_users()
    except ObjectNotFound as ex:
        # no users defined
        userl = []
    user = API.add_user(name=USER_NAME)
    assert (user.data['name'] == USER_NAME)
    userl2 = API.list_users()
    assert (len(userl2) == len(userl) + 1)
    assert (userl2.count(USER_NAME) == 1)


def test_list_users():
    userl = API.list_users()
    assert (userl is not None)


def test_object_already_exists():
    try:
        user = API.add_user(name=USER_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_user():
    user = API.get_user(USER_NAME)
    assert (user.data['name'] == USER_NAME)


def test_generate_user_from_json():
    user = API.get_user(USER_NAME)
    json = user.to_json()
    user2 = API.generate_object(json)
    assert (user2.__class__.__name__ == user.__class__.__name__)
    for key in list(user.data.keys()):
        v = user.data[key]
        v2 = user2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_user():
    user = API.get_user(USER_NAME)
    oticket = user.data['oticket']
    user = API.modify_user(name=USER_NAME, data={'oticket': oticket + 1})
    oticket2 = user.data['oticket']
    assert (oticket2 == oticket + 1)


def test_delete_user():
    userl = API.list_users()
    API.delete_user(USER_NAME)
    try:
        userl2 = API.list_users()
    except ObjectNotFound as ex:
        # no users defined
        userl2 = []
    assert (len(userl2) == len(userl) - 1)
    assert (userl2.count(USER_NAME) == 0)
