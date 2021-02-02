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
import types
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
RQS_NAME = 'rqs%s' % generate_random_string(6)


@needs_uge
def test_object_not_found():
    try:
        rqs = API.get_rqs('__non_existent_rqs__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_rqs():
    rqs = API.generate_rqs(RQS_NAME)
    assert (rqs.data['name'] == RQS_NAME)


def test_add_rqs():
    rqs_list = API.list_rqss()
    rqs = API.add_rqs(name=RQS_NAME)
    assert (rqs.data['name'] == RQS_NAME)
    rqs_list2 = API.list_rqss()
    assert (len(rqs_list2) == len(rqs_list) + 1)
    assert (rqs_list2.count(RQS_NAME) == 1)


def test_list_rqss():
    rqs_list = API.list_rqss()
    assert (rqs_list is not None)


def test_object_already_exists():
    try:
        rqs = API.add_rqs(name=RQS_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_rqs():
    rqs = API.get_rqs(RQS_NAME)
    assert (rqs.data['name'] == RQS_NAME)


def test_generate_rqs_from_json():
    rqs = API.get_rqs(RQS_NAME)
    json = rqs.to_json()
    rqs2 = API.generate_object(json)
    assert (rqs2.__class__.__name__ == rqs.__class__.__name__)
    for key in list(rqs.data.keys()):
        v = rqs.data[key]
        v2 = rqs2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_rqs():
    rqs = API.get_rqs(RQS_NAME)
    enabled = rqs.data['enabled']
    rqs = API.modify_rqs(name=RQS_NAME, data={'enabled': not enabled})
    enabled2 = rqs.data['enabled']
    assert (enabled2 == (not enabled))


def test_delete_rqs():
    rqs_list = API.list_rqss()
    API.delete_rqs(RQS_NAME)
    rqs_list2 = API.list_rqss()
    assert (len(rqs_list2) == len(rqs_list) - 1)
    assert (rqs_list2.count(RQS_NAME) == 0)
