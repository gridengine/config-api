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
PE_NAME = '%s.q' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


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


def test_get_acls():
    pel = API.list_pes()
    pes = API.get_pes()
    for pe in pes:
        print("#############################################")
        print(pe.to_uge())
        assert (pe.data['pe_name'] in pel)

def test_write_pes():
    try:
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        pe_names = VALUES_DICT['pe_names']
        pes = API.get_pes()
        for pe in pes:
            print("Before #############################################")
            print(pe.to_uge())

        new_pes = []
        for name in pe_names:
            npe = API.generate_pe(name=name)
            new_pes.append(npe)
        API.mk_pes_dir(tdir)
        API.write_pes(new_pes, tdir)
        API.add_pes_from_dir(tdir)
        API.modify_pes_from_dir(tdir)
        pes = API.get_pes()
        for pe in pes:
            print("After #############################################")
            print(pe.to_uge())

        pes = API.list_pes()
        for name in pe_names:
            assert (name in pes)
            print("pe found: " + name)

    finally:
        API.delete_pes_from_dir(tdir)
        API.rm_pes_dir(tdir)


def test_add_pes():
    try:
        new_pes = []
        pe_names = VALUES_DICT['pe_names']
        for name in pe_names:
            npe = API.generate_pe(name=name)
            new_pes.append(npe)

        # print all pes currently in the cluster
        pes = API.get_pes()
        for pe in pes:
            print("Before #############################################")
            print(pe.to_uge())

        # add pes
        API.add_pes(new_pes)
        API.modify_pes(new_pes)

        # print all pes currently in the cluster
        pes = API.get_pes()
        for pe in pes:
            print("After #############################################")
            print(pe.to_uge())

        # check that cals have been added
        pes = API.list_pes()
        for name in pe_names:
            assert (name in pes)
            print("pe found: " + name)

    finally:
        API.delete_pes(new_pes)


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
