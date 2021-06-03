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
QUEUE_NAME = '%s.q' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


@needs_uge
def test_object_not_found():
    try:
        q = API.get_queue('__non_existent__.q')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_queue():
    q = API.generate_queue(QUEUE_NAME)
    assert (q.data['qname'] == QUEUE_NAME)


def test_list_queues():
    ql = API.list_queues()
    assert (ql is not None)


def test_add_queue():
    ql = API.list_queues()
    q = API.add_queue(name=QUEUE_NAME)
    assert (q.data['qname'] == QUEUE_NAME)
    ql2 = API.list_queues()
    assert (len(ql2) == len(ql) + 1)
    assert (ql2.count(QUEUE_NAME) == 1)


def test_object_already_exists():
    try:
        q = API.add_queue(name=QUEUE_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_queue():
    q = API.get_queue(QUEUE_NAME)
    assert (q.data['qname'] == QUEUE_NAME)


def test_generate_queue_from_json():
    queue = API.get_queue(QUEUE_NAME)
    json = queue.to_json()
    queue2 = API.generate_object(json)
    assert (queue2.__class__.__name__ == queue.__class__.__name__)
    for key in list(queue.data.keys()):
        v = queue.data[key]
        v2 = queue2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_queue():
    q = API.get_queue(QUEUE_NAME)
    slots = int(q.data['slots'][0])
    q = API.modify_queue(name=QUEUE_NAME, data={'slots': [str(slots + 1)]})
    slots2 = int(q.data['slots'][0])
    assert (slots2 == slots + 1)


def test_get_queue():
    queuel = API.list_queues()
    queues = API.get_queues()
    for queue in queues:
        print("#############################################")
        print(queue.to_uge())
        assert (queue.data['qname'] in queuel)


def test_write_queues():
    try:
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        queue_names = VALUES_DICT['queue_names']
        queues = API.get_queues()
        for queue in queues:
            print("Before #############################################")
            print(queue.to_uge())

        new_queues = []
        for name in queue_names:
            nqueue = API.generate_queue(name=name)
            new_queues.append(nqueue)
        API.mk_queues_dir(tdir)
        API.write_queues(new_queues, tdir)
        API.add_queues_from_dir(tdir)
        API.modify_queues_from_dir(tdir)
        queues = API.get_queues()
        for queue in queues:
            print("After #############################################")
            print(queue.to_uge())

        queues = API.list_queues()
        for name in queue_names:
            assert (name in queues)
            print("queue found: " + name)

    finally:
        API.delete_queues_from_dir(tdir)
        API.rm_queues_dir(tdir)


def test_add_queues():
    try:
        new_queues = []
        queue_names = VALUES_DICT['queue_names']
        for name in queue_names:
            nqueue = API.generate_queue(name=name)
            new_queues.append(nqueue)

        # print all queues currently in the cluster
        queues = API.get_queues()
        for queue in queues:
            print("Before #############################################")
            print(queue.to_uge())

        # add queues
        API.add_queues(new_queues)
        API.modify_queues(new_queues)

        # print all queues currently in the cluster
        queues = API.get_queues()
        for queue in queues:
            print("After #############################################")
            print(queue.to_uge())

        # check that queues have been added
        queues = API.list_queues()
        for name in queue_names:
            assert (name in queues)
            print("queue found: " + name)

    finally:
        API.delete_queues(new_queues)


def test_delete_queue():
    ql = API.list_queues()
    API.delete_queue(QUEUE_NAME)
    ql2 = API.list_queues()
    assert (len(ql2) == len(ql) - 1)
    assert (ql2.count(QUEUE_NAME) == 0)
