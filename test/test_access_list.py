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

from .utils import needs_uge
from .utils import generate_random_string
from .utils import generate_random_string_list
from .utils import create_config_file
from .utils import load_values

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
ACL_NAME = 'acl.%s' % generate_random_string(6)
USER1_NAME = 'user.%s' % generate_random_string(6)
USER2_NAME = 'user.%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


@needs_uge
def test_object_not_found():
    try:
        acl = API.get_acl('__non_existent_acl__')
        assert(False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_acl():
    acl = API.generate_acl(ACL_NAME)
    assert(acl.data['name'] == ACL_NAME)


def test_add_acl():
    try:
        acl_list = API.list_acls()
    except ObjectNotFound as ex:
        # no acls defined
        acl_list = []
    acl = API.add_acl(name=ACL_NAME)
    assert(acl.data['name'] == ACL_NAME)
    acl_list2 = API.list_acls()
    assert(len(acl_list2) == len(acl_list) + 1)
    assert(acl_list2.count(ACL_NAME) == 1)


def test_list_acls():
    acl_list = API.list_acls()
    assert(acl_list is not None)


def test_object_already_exists():
    try:
        acl = API.add_acl(name=ACL_NAME)
        assert(False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_acl():
    acl = API.get_acl(ACL_NAME)
    assert(acl.data['name'] == ACL_NAME)


def test_generate_acl_from_json():
    acl = API.get_acl(ACL_NAME)
    assert(acl.data['name'] == ACL_NAME)
    json = acl.to_json()
    acl2 = API.generate_object(json)
    assert(acl2.__class__.__name__ == acl.__class__.__name__)
    for key in list(acl.data.keys()):
        v = acl.data[key]
        v2 = acl2.data[key]
        assert(str(v) == str(v2))


def test_modify_acl():
    acl = API.get_acl(ACL_NAME)
    acl = API.modify_acl(name=ACL_NAME, data={'entries' : [USER1_NAME, USER2_NAME]})
    entries = acl.data['entries']
    assert(len(entries) == 2)


def test_get_acls():
    acll = API.list_acls()
    acls = API.get_acls()
    for acl in acls:
        print("#############################################")
        print(acl.to_uge())
        assert (acl.data['name'] in acll)


def test_write_acls():
    try:
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        acl_names = VALUES_DICT['acl_names']
        acls = API.get_acls()
        for acl in acls:
            print("Before #############################################")
            print(acl.to_uge())

        new_acls = []
        for name in acl_names:
            nacl = API.generate_acl(name=name)
            new_acls.append(nacl)
        API.mk_acls_dir(tdir)
        API.write_acls(new_acls, tdir)
        API.add_acls_from_dir(tdir)
        API.modify_acls_from_dir(tdir)
        acls = API.get_acls()
        for acl in acls:
            print("After #############################################")
            print(acl.to_uge())

        acls = API.list_acls()
        for name in acl_names:
            assert (name in acls)
            print("acl found: " + name)

    finally:
        API.delete_acls_from_dir(tdir)
        API.rm_acls_dir(tdir)


def test_add_acls():
    try:
        new_acls = []
        acl_names = VALUES_DICT['acl_names']
        for name in acl_names:
            nacl = API.generate_acl(name=name)
            new_acls.append(nacl)

        # print all acls currently in the cluster
        acls = API.get_acls()
        for acl in acls:
            print("Before #############################################")
            print(acl.to_uge())

        # add acls
        API.add_acls(new_acls)
        API.modify_acls(new_acls)

        # print all acls currently in the cluster
        acls = API.get_acls()
        for acl in acls:
            print("After #############################################")
            print(acl.to_uge())

        # check that cals have been added
        acls = API.list_acls()
        for name in acl_names:
            assert (name in acls)
            print("acl found: " + name)

    finally:
        API.delete_acls(new_acls)


def test_add_users_to_acl_and_delete_users_from_acl():
    acl_list = API.list_acls()
    n_acls = 3
    n_users = 3
    acl_name_list = generate_random_string_list(n_strings=3, string_length=6, delimiter=',', string_prefix='acl.')
    user_name_list = generate_random_string_list(n_strings=3, string_length=6, delimiter=',', string_prefix='user.')
    new_acls = API.add_users_to_acls(user_name_list, acl_name_list)
    assert(len(new_acls) == n_acls)
    for i in range (0,n_acls):
        assert(len(new_acls[i].data['entries']) == n_users)
    acl_list2 = API.list_acls()
    assert(len(acl_list2) == len(acl_list) + n_acls)
    modified_acls = API.delete_users_from_acls(user_name_list, acl_name_list)
    for i in range (0,n_acls):
        assert(modified_acls[i].data['entries'] is None)
    for i in range (0,n_acls):
        API.delete_acl(modified_acls[i].data['name'])
    acl_list3 = API.list_acls()
    assert(len(acl_list3) == len(acl_list))


def test_delete_acl():
    acl_list = API.list_acls()
    API.delete_acl(ACL_NAME)
    try:
        acl_list2 = API.list_acls()
    except ObjectNotFound as ex:
        # no acls defined
        acl_list2 = []
    assert(len(acl_list2) == len(acl_list) - 1)
    assert(acl_list2.count(ACL_NAME) == 0)
