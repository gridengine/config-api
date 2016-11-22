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
import types
from utils import needs_uge
from utils import generate_random_string
from utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
PROJECT_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()

@needs_uge
def test_object_not_found():
    try:
        project = API.get_prj('__non_existent_project__')
        assert(False)
    except ObjectNotFound, ex:
        # ok
        pass

def test_generate_prj():
    project = API.generate_prj(PROJECT_NAME)
    assert(project.data['name'] == PROJECT_NAME)

def test_add_prj():
    try:
        project_list = API.list_prjs()
    except ObjectNotFound, ex:
        # no projects defined
        project_list = []
    project = API.add_prj(name=PROJECT_NAME)
    assert(project.data['name'] == PROJECT_NAME)
    project_list2 = API.list_prjs()
    assert(len(project_list2) == len(project_list) + 1)
    assert(project_list2.count(PROJECT_NAME) == 1)

def test_list_prjs():
    project_list = API.list_prjs()
    assert(project_list is not None)

def test_object_already_exists():
    try:
        project = API.add_prj(name=PROJECT_NAME)
        assert(False)
    except ObjectAlreadyExists, ex:
        # ok
        pass

def test_get_prj():
    project = API.get_prj(PROJECT_NAME)
    assert(project.data['name'] == PROJECT_NAME)

def test_generate_prj_from_json():
    prj = API.get_prj(PROJECT_NAME)
    json = prj.to_json()
    prj2 = API.generate_object(json)
    assert(prj2.__class__.__name__ == prj.__class__.__name__)
    for key in prj.data.keys():
        v = prj.data[key]
        v2 = prj2.data[key]
        if type(v) == types.ListType:
            assert(len(v) == len(v2))
            for s in v:
                assert(v2.count(s) == 1)
        elif type(v) == types.DictType:
            for key in v.keys():
                assert(str(v[key]) == str(v2[key]))
        else:
            assert(str(v) == str(v2))

def test_modify_prj():
    project = API.get_prj(PROJECT_NAME)
    oticket = project.data['oticket'] 
    project = API.modify_prj(name=PROJECT_NAME, data={'oticket' : oticket + 1})
    oticket2 = project.data['oticket'] 
    assert(oticket2 == oticket+1)

def test_delete_prj():
    project_list = API.list_prjs()
    API.delete_prj(PROJECT_NAME)
    try:
        project_list2 = API.list_prjs()
    except ObjectNotFound, ex:
        # no projects defined
        project_list2 = []
    assert(len(project_list2) == len(project_list) - 1)
    assert(project_list2.count(PROJECT_NAME) == 0)

