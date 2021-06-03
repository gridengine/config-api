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

import tempfile
import types
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
HOST_GROUP_NAME = '@%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
HOST_NAME = CONFIG_MANAGER['host']
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


@needs_uge
def test_generate_hgrp():
    hgrp = API.generate_hgrp(HOST_GROUP_NAME)
    assert (hgrp.data['group_name'] == HOST_GROUP_NAME)


def test_list_hgrps():
    hgrpl = API.list_hgrps()
    assert (hgrpl is not None)


def test_add_hgrp():
    hgrp = API.add_hgrp(name=HOST_GROUP_NAME, data={'hostlist': HOST_NAME})
    assert (hgrp.data['group_name'] == HOST_GROUP_NAME)


def test_object_already_exists():
    try:
        hgrpl = API.list_hgrps()
        if len(hgrpl):
            hgrp = API.add_hgrp(name=hgrpl[0])
            assert (False)
        else:
            raise SkipTest('There are no configured UGE host groups.')
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_object_not_found():
    try:
        hgrp = API.get_hgrp('__non_existent_host_group__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_get_hgrp():
    hgrpl = API.list_hgrps()
    if len(hgrpl):
        hgrp = API.get_hgrp(hgrpl[0])
        assert (hgrp.data['group_name'] == hgrpl[0])
    else:
        raise SkipTest('There are no configured UGE host groups.')


def test_generate_hgrp_from_json():
    hgrpl = API.list_hgrps()
    if len(hgrpl):
        hgrp = API.get_hgrp(hgrpl[0])
    else:
        raise SkipTest('There are no configured UGE host groups.')

    json = hgrp.to_json()
    hgrp2 = API.generate_object(json)
    assert (hgrp2.__class__.__name__ == hgrp.__class__.__name__)
    for key in list(hgrp.data.keys()):
        v = hgrp.data[key]
        v2 = hgrp2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)


def test_modify_hgrp():
    hgrpl = API.list_hgrps()
    if len(hgrpl):
        hgrp = API.get_hgrp(hgrpl[0])
        original_host_list = hgrp.data['hostlist']
        hgrp2 = API.modify_hgrp(name=hgrpl[0], data={'hostlist': HOST_NAME})
        assert (hgrp2.data['hostlist'].count(HOST_NAME) == 1)
        hgrp3 = API.modify_hgrp(name=hgrpl[0], data={'hostlist': original_host_list})
        assert (hgrp3.data['hostlist'] == original_host_list)
    else:
        raise SkipTest('There are no configured UGE host groups.')


def test_get_hgrps():
    hgrpl = API.list_hgrps()
    hgrps = API.get_hgrps()
    for hgrp in hgrps:
        print("#############################################")
        print(hgrp.to_uge())
        assert (hgrp.data['group_name'] in hgrpl)


def test_write_hgrps():
    try:
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        hgrp_names = VALUES_DICT['hgrp_names']
        hgrps = API.get_hgrps()
        for hgrp in hgrps:
            print("Before #############################################")
            print(hgrp.to_uge())

        new_hgrps = []
        for name in hgrp_names:
            nhgrp = API.generate_hgrp(name=name)
            new_hgrps.append(nhgrp)
        API.mk_hgrps_dir(tdir)
        API.write_hgrps(new_hgrps, tdir)
        API.add_hgrps_from_dir(tdir)
        API.modify_hgrps_from_dir(tdir)
        hgrps = API.get_hgrps()
        for hgrp in hgrps:
            print("After #############################################")
            print(hgrp.to_uge())

        hgrps = API.list_hgrps()
        for name in hgrp_names:
            assert (name in hgrps)
            print("host group found: " + name)

    finally:
        API.delete_hgrps_from_dir(tdir)
        API.rm_hgrps_dir(tdir)


def test_add_hgrps():
    try:
        new_hgrps = []
        hgrp_names = VALUES_DICT['hgrp_names']
        for name in hgrp_names:
            nhgrp = API.generate_hgrp(name=name)
            new_hgrps.append(nhgrp)

        # print all host groups currently in the cluster
        hgrps = API.get_hgrps()
        for hgrp in hgrps:
            print("Before #############################################")
            print(hgrp.to_uge())

        # add host groups
        API.add_hgrps(new_hgrps)
        API.modify_hgrps(new_hgrps)

        # print all host groups currently in the cluster
        hgrps = API.get_hgrps()
        for hgrp in hgrps:
            print("After #############################################")
            print(hgrp.to_uge())

        # check that host groups have been added
        hgrps = API.list_hgrps()
        for name in hgrp_names:
            assert (name in hgrps)
            print("host group found: " + name)

    finally:
        API.delete_hgrps(new_hgrps)


def test_delete_hgrp():
    hgrpl = API.list_hgrps()
    if hgrpl.count(HOST_GROUP_NAME):
        API.delete_hgrp(HOST_GROUP_NAME)
        hgrpl2 = API.list_hgrps()
        assert (hgrpl2.count(HOST_GROUP_NAME) == 0)
    else:
        raise SkipTest('There UGE host group %s has not been added.' % HOST_GROUP_NAME)
