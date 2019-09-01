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
PE_NAME = '%s.q' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_object_not_found():
    try:
        pe = API.get_pe('__non_existent_pe__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_pe():
    pe = API.generate_pe(PE_NAME)
    assert (pe.data['pe_name'] == PE_NAME)


def test_add_pe():
    try:
        pel = API.list_pes()
    except ObjectNotFound as ex:
        # no pes defined
        pel = []
    pe = API.add_pe(name=PE_NAME)
    assert (pe.data['pe_name'] == PE_NAME)
    pel2 = API.list_pes()
    assert (len(pel2) == len(pel) + 1)
    assert (pel2.count(PE_NAME) == 1)


def test_list_pes():
    pel = API.list_pes()
    assert (pel is not None)


def test_object_already_exists():
    try:
        pe = API.add_pe(name=PE_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_pe():
    pe = API.get_pe(PE_NAME)
    assert (pe.data['pe_name'] == PE_NAME)


def test_generate_pe_from_json():
    pe = API.get_pe(PE_NAME)
    json = pe.to_json()
    pe2 = API.generate_object(json)
    assert (pe2.__class__.__name__ == pe.__class__.__name__)
    for key in list(pe.data.keys()):
        v = pe.data[key]
        v2 = pe2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_pe():
    pe = API.get_pe(PE_NAME)
    slots = pe.data['slots']
    pe = API.modify_pe(name=PE_NAME, data={'slots': slots + 1})
    slots2 = pe.data['slots']
    assert (slots2 == slots + 1)


def test_delete_pe():
    pel = API.list_pes()
    API.delete_pe(PE_NAME)
    try:
        pel2 = API.list_pes()
    except ObjectNotFound as ex:
        # no pes defined
        pel2 = []
    assert (len(pel2) == len(pel) - 1)
    assert (pel2.count(PE_NAME) == 0)
