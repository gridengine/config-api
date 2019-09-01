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
JC_NAME = 'jc%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_object_not_found():
    try:
        jc = API.get_jc('__non_existent_jc__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_jc():
    jc = API.generate_jc(JC_NAME)
    assert (jc.data['jcname'] == JC_NAME)


def test_add_jc():
    jc_list = API.list_jcs()
    jc = API.add_jc(name=JC_NAME)
    assert (jc.data['jcname'] == JC_NAME)
    jc_list2 = API.list_jcs()
    assert (len(jc_list2) == len(jc_list) + 1)
    assert (jc_list2.count(JC_NAME) == 1)


def test_list_jcs():
    jc_list = API.list_jcs()
    assert (jc_list is not None)


def test_object_already_exists():
    try:
        jc = API.add_jc(name=JC_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_jc():
    jc = API.get_jc(JC_NAME)
    assert (jc.data['jcname'] == JC_NAME)


def test_generate_jc_from_json():
    jc = API.get_jc(JC_NAME)
    json = jc.to_json()
    jc2 = API.generate_object(json)
    assert (jc2.__class__.__name__ == jc.__class__.__name__)
    for key in list(jc.data.keys()):
        v = jc.data[key]
        v2 = jc2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_jc():
    jc = API.get_jc(JC_NAME)
    jc = API.modify_jc(name=JC_NAME, data={'CMDNAME': '/bin/ls'})
    shell = jc.data['CMDNAME']
    assert (shell == '/bin/ls')


def test_delete_jc():
    jc_list = API.list_jcs()
    API.delete_jc(JC_NAME)
    jc_list2 = API.list_jcs()
    assert (len(jc_list2) == len(jc_list) - 1)
    assert (jc_list2.count(JC_NAME) == 0)
