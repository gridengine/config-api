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
import copy
import random
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.qconf_api import QconfApi

create_config_file()
API = QconfApi()
CATTR_NAME = 'z%s' % generate_random_string(6)
CATTR_URGENCY = int(random.uniform(0, 100))


@needs_uge
def test_generate_cconf():
    cconf = API.generate_cconf()
    assert ('slots' in cconf.data)


def test_get_cconf():
    cconf = API.get_cconf()
    assert ('slots' in cconf.data)


def test_generate_cconf_from_json():
    cconf = API.get_cconf()
    json = cconf.to_json()
    cconf2 = API.generate_object(json)
    assert (cconf2.__class__.__name__ == cconf.__class__.__name__)
    for key in list(cconf.data.keys()):
        v = cconf.data[key]
        v2 = cconf2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_cconf():
    cconf = API.get_cconf()
    slots = cconf.data['slots']
    urgency = slots['urgency']
    slots2 = copy.copy(slots)
    slots2['urgency'] = slots['urgency'] + 1
    cconf2 = API.modify_cconf(data={'slots': slots2})
    urgency2 = cconf2.data['slots']['urgency']
    assert (urgency2 == urgency + 1)
    cconf3 = API.modify_cconf(data={'slots': slots})
    urgency3 = cconf3.data['slots']['urgency']
    assert (urgency3 == urgency)


def test_add_cattr():
    cattr_data = {'shortcut': CATTR_NAME[0:3], 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': True,
                  'default': 10, 'urgency': CATTR_URGENCY, 'aapre': False, 'affinity': 0.1,
                  'do_report': True, 'is_static': False}
    cconf = API.add_cattr(CATTR_NAME, cattr_data)
    assert (cconf.data[CATTR_NAME]['urgency'] == CATTR_URGENCY)


def test_modify_cattr():
    cconf = API.get_cconf()
    cattr_data = cconf.data[CATTR_NAME]
    assert (cattr_data['urgency'] == CATTR_URGENCY)
    cattr_data['urgency'] = 2 * CATTR_URGENCY
    cconf = API.modify_cattr(CATTR_NAME, cattr_data)
    assert (cconf.data[CATTR_NAME]['urgency'] == 2 * CATTR_URGENCY)


def test_delete_cattr():
    cconf = API.get_cconf()
    assert (CATTR_NAME in cconf.data)
    cconf = API.delete_cattr(CATTR_NAME)
    assert (CATTR_NAME not in cconf.data)
