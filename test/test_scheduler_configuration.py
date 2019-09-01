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

create_config_file()
API = QconfApi()


@needs_uge
def test_generate_sconf():
    sconf = API.generate_sconf()
    assert ('schedule_interval' in sconf.data)


def test_get_sconf():
    sconf = API.get_sconf()
    assert ('schedule_interval' in sconf.data)


def test_generate_sconf_from_json():
    sconf = API.get_sconf()
    json = sconf.to_json()
    sconf2 = API.generate_object(json)
    assert (sconf2.__class__.__name__ == sconf.__class__.__name__)
    for key in list(sconf.data.keys()):
        v = sconf.data[key]
        v2 = sconf2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_sconf():
    sconf = API.get_sconf()
    weight_user = sconf.data['weight_user']
    sconf = API.modify_sconf(data={'weight_user': weight_user * 2})
    weight_user2 = sconf.data['weight_user']
    assert (weight_user2 == weight_user * 2)
    sconf = API.modify_sconf(data={'weight_user': weight_user})
    weight_user3 = sconf.data['weight_user']
    assert (weight_user3 == weight_user)
