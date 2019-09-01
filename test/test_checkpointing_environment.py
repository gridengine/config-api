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
CKPT_NAME = '%s.q' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_object_not_found():
    try:
        pe = API.get_ckpt('__non_existent_ckpt__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_ckpt():
    ckpt = API.generate_ckpt(CKPT_NAME)
    assert (ckpt.data['ckpt_name'] == CKPT_NAME)


def test_add_ckpt():
    try:
        ckptl = API.list_ckpts()
    except ObjectNotFound as ex:
        # no ckpts defined
        ckptl = []
    ckpt = API.add_ckpt(name=CKPT_NAME)
    assert (ckpt.data['ckpt_name'] == CKPT_NAME)
    ckptl2 = API.list_ckpts()
    assert (len(ckptl2) == len(ckptl) + 1)
    assert (ckptl2.count(CKPT_NAME) == 1)


def test_list_ckpts():
    ckptl = API.list_ckpts()
    assert (ckptl is not None)


def test_object_already_exists():
    try:
        ckpt = API.add_ckpt(name=CKPT_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_ckpt():
    ckpt = API.get_ckpt(CKPT_NAME)
    assert (ckpt.data['ckpt_name'] == CKPT_NAME)


def test_generate_ckpt_from_json():
    ckpt = API.get_ckpt(CKPT_NAME)
    assert (ckpt.data['ckpt_name'] == CKPT_NAME)
    json = ckpt.to_json()
    ckpt2 = API.generate_object(json)
    assert (ckpt2.__class__.__name__ == ckpt.__class__.__name__)
    for key in list(ckpt.data.keys()):
        v = ckpt.data[key]
        v2 = ckpt2.data[key]
        assert (str(v) == str(v2))


def test_modify_ckpt():
    ckpt = API.get_ckpt(CKPT_NAME)
    ckpt_dir = ckpt.data['ckpt_dir']
    ckpt = API.modify_ckpt(name=CKPT_NAME, data={'ckpt_dir': '/storage'})
    ckpt_dir2 = ckpt.data['ckpt_dir']
    assert (ckpt_dir2 == '/storage')


def test_delete_ckpt():
    ckptl = API.list_ckpts()
    API.delete_ckpt(CKPT_NAME)
    try:
        ckptl2 = API.list_ckpts()
    except ObjectNotFound as ex:
        # no ckpts defined
        ckptl2 = []
    assert (len(ckptl2) == len(ckptl) - 1)
    assert (ckptl2.count(CKPT_NAME) == 0)
