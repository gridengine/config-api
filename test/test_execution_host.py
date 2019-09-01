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

import tempfile

from nose import SkipTest

from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file
from .utils import load_values

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
HOST_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


@needs_uge
def test_generate_ehost():
    h = API.generate_ehost(HOST_NAME)
    assert (h.data['hostname'] == HOST_NAME)


def test_list_ehosts():
    hl = API.list_ehosts()
    assert (hl is not None)


def test_object_already_exists():
    try:
        hl = API.list_ehosts()
        if len(hl):
            h = API.add_ehost(name=hl[0])
            assert (False)
        else:
            raise SkipTest('There are no configured UGE execution hosts.')
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_ehost():
    hl = API.list_ehosts()
    if len(hl):
        h = API.get_ehost(hl[0])
        assert (h.data['hostname'] == hl[0])
    else:
        raise SkipTest('There are no configured UGE execution hosts.')


def test_modify_ehost():
    hl = API.list_ehosts()
    if len(hl):
        h = API.get_ehost(hl[0])
        original_complex_values = h.data['complex_values']
        new_complex_values = ['slots=100']
        h2 = API.modify_ehost(name=hl[0], data={'complex_values': new_complex_values})
        output_string = '%s' % h2.data['complex_values']
        input_string = '%s' % new_complex_values
        assert (input_string == output_string)
        h3 = API.modify_ehost(name=hl[0], data={'complex_values': original_complex_values})
        output_string = '%s' % h3.data['complex_values']
        input_string = '%s' % original_complex_values
        assert (input_string == output_string)
    else:
        raise SkipTest('There are no configured UGE execution hosts.')


def test_get_ehosts():
    ehl = API.list_ehosts()
    ehosts = API.get_ehosts()
    for eh in ehosts:
        print("#############################################")
        print(eh.to_uge())
        assert (eh.data['hostname'] in ehl)


def test_write_ehosts():
    try:
        # tdir = '/tmp/uge/ehosts'
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        host_names = VALUES_DICT['host_names']
        ehosts = API.get_ehosts()
        for eh in ehosts:
            print("Before #############################################")
            print(eh.to_uge())

        add_hosts = []
        for name in host_names:
            neh = API.generate_ehost(name=name)
            add_hosts.append(neh)
        API.mk_ehosts_dir(tdir)
        API.write_ehosts(add_hosts, tdir)
        API.add_ehosts_from_dir(tdir)
        API.modify_ehosts_from_dir(tdir)
        ehosts = API.get_ehosts()
        for eh in ehosts:
            print("After #############################################")
            print(eh.to_uge())
    finally:
        API.delete_ehosts(host_names)
        API.rm_ehosts_dir(tdir)


def test_add_ehosts():
    try:
        add_hosts = []
        host_names = VALUES_DICT['host_names']
        for name in host_names:
            neh = API.generate_ehost(name=name)
            add_hosts.append(neh)

        # print all execution hosts currently in the cluster
        ehosts = API.get_ehosts()
        for eh in ehosts:
            print("Before #############################################")
            print(eh.to_uge())

        # add execution hosts
        API.add_ehosts(add_hosts)

        # print all execution hosts currently in the cluster
        ehosts = API.get_ehosts()
        for eh in ehosts:
            print("After #############################################")
            print(eh.to_uge())

        # check that hosts have been added
        ehosts = API.list_ehosts()
        for h in host_names:
            assert (h in ehosts)
            print("execution host found: " + h)

    finally:
        API.delete_ehosts(host_names)
